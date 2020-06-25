#!/usr/bin/env python2.7
import matplotlib as mpl
mpl.use('Agg')
import os, shutil, fileinput, tarfile, subprocess
import labels, sed, modularized_model_main, tar_to_record, export
from os.path import join

outputdir = '/opt/ml/model/finished-models'
trainpath = 'learn/train/'

def logstatus(message):
    print(message)
    with open('status.txt','w') as status:
        status.write(message)

def main(name, TRAIN_STEPS, BATCH_SIZE, checkpoint, data_set_path, steps_per_eval=100):

    shutil.rmtree(trainpath, ignore_errors=True)
    os.mkdir(trainpath)

    logstatus('preparing the dataset')
    tar_to_record.main(data_set_path, '/opt/ml/input/data/training/')

    with open('pipeline.config') as config:
        config = config.read()
        if '/tensorflow/models/research/learn/ckpt/%s/model.ckpt'%(checkpoint) not in config:
            sed.replace_words('/tensorflow/models/research/learn/ckpt/ssd_mobilenet_v2_quantized_300x300_coco_2019_01_03/model.ckpt',
                '/tensorflow/models/research/learn/ckpt/%s/model.ckpt'%(checkpoint), "pipeline.config")
    
    classes = labels.get()
    sed.replace_words('NUM_CLASSES', str(classes), "pipeline.config")
    sed.replace_words('BATCH_SIZE_PARAM', str(BATCH_SIZE), "pipeline.config")
    shutil.copy('pipeline.config','learn/ckpt/pipeline.config')

    logstatus('training the model')
    modularized_model_main.main(
        pipeline_config_path='learn/ckpt/pipeline.config',
        model_dir=trainpath,
        num_train_steps=TRAIN_STEPS,
        eval_period=steps_per_eval)

    export.main(TRAIN_STEPS, outputdir, name)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--name', help='The desired model name.', type=str, default='model')
    parser.add_argument('-s', '--steps', help='The desired amount of training steps.', type=int, default = 100)
    parser.add_argument('-b', '--batch', help='The desired batch size.', type=int, default = 32)
    parser.add_argument('-ptm', '--checkpoint', help='The name of the model you wish to retrain', type=str, default = 'mobilenet_v2_ssd')
    parser.add_argument('-dsp', '--dataset', help='The path to the dataset', type=str, default = '/opt/ml/input/data/training/full_data.tar')
    parser.add_argument('-ep', '--eval_period', help='How many epochs to run before running another evaluation', type=int, default = 100)
    args = parser.parse_args()
    main(args.name,args.steps,args.batch,args.checkpoint,args.dataset,args.eval_period)
