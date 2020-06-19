#!/usr/bin/env python2.7

import os, shutil, fileinput, tarfile, subprocess
import labels, sed, modularized_model_main, tar_to_record
from os.path import join
ckpt_name_map={}
ckpt_name_map["mobilenet_v1_ssd"]="ssd_mobilenet_v1_quantized_300x300_coco14_sync_2018_07_18"
ckpt_name_map["mobilenet_v2_ssd"]="ssd_mobilenet_v2_quantized_300x300_coco_2019_01_03"

def logstatus(message):
    print(message)
    with open('status.txt','w') as status:
        status.write(message)

def main(name, steps, batch, premodel, data_set_path, steps_per_eval=100):

    TRAIN_STEPS = steps
    BATCH_SIZE = batch
    OUTPUT_NAME = '%s.tar.gz'%(name)
    outputdir = '/opt/ml/model/'

    if ckpt_name_map[premodel] not in os.listdir('learn/ckpt'):
        logstatus('downloading pre-trained model %s'%(premodel))
        subprocess.call(['bash','switch_checkpoint.sh',premodel])

    logstatus('preparing the dataset')
    tar_to_record.main(data_set_path, '/opt/ml/input/data/training/')

    #must make function to switch to the pretrained models specific .config
    classes = labels.get()
    sed.replace_words('NUM_CLASSES', str(classes), "pipeline.config")
    sed.replace_words('BATCH_SIZE_PARAM', str(BATCH_SIZE), "pipeline.config")

    shutil.copy('pipeline.config','learn/ckpt/pipeline.config')
    shutil.rmtree('learn/train', ignore_errors=True)
    os.mkdir('learn/train')

    # here we should write the class tags of
    # /opt/ml/input/data/training/Raw Data/meta.json to a labelmap file.
    with open('labels.txt', 'w') as labelfile:
        labelfile.writelines(['0 powercell'])

    logstatus('training the model')
    modularized_model_main.main(
        pipeline_config_path='learn/ckpt/pipeline.config',
        model_dir='learn/train',
        num_train_steps=TRAIN_STEPS,
        eval_period=steps_per_eval)

    logstatus('converting model to tflite')
    subprocess.check_call("./convert_checkpoint_to_edgetpu_tflite.sh --checkpoint_num %s" % (str(TRAIN_STEPS)),
                          shell=True)
    shutil.copy('learn/models/output_tflite_graph.tflite', join(outputdir,'unoptimized.tflite'))

    logstatus('compiling model for edgetpu')
    subprocess.check_call("edgetpu_compiler ./learn/models/output_tflite_graph.tflite -o %s"%(outputdir), shell=True)

    logstatus('compressing model to tar')
    with tarfile.open(join(outputdir,OUTPUT_NAME),'w:gz') as model:
        model.add(join(outputdir,'output_tflite_graph_edgetpu.tflite'),arcname='model.tflite')
        model.add('/opt/ml/input/data/training/map.pbtxt',arcname='map.pbtxt')
        model.add(join(outputdir,'unoptimized.tflite'),arcname='unoptimized.tflite')

    logstatus('Finished! Get your model.')

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--name', help='The desired model name.', type=str, default='model')
    parser.add_argument('-s', '--steps', help='The desired amount of training steps.', type=int, default = 100)
    parser.add_argument('-b', '--batch', help='The desired batch size.', type=int, default = 32)
    parser.add_argument('-ptm', '--premodel', help='The name of the model you wish to retrain', type=str, default = 'mobilenet_v2_ssd')
    parser.add_argument('-dsp', '--dataset', help='The path to the dataset', type=str, default = '/opt/ml/input/data/training/full_data.tar')
    parser.add_argument('-ep', '--eval_period', help='How many epochs to run before running another evaluation', type=int, default = 100)
    args = parser.parse_args()
    main(args.name,args.steps,args.batch,args.premodel,args.dataset,args.eval_period)
