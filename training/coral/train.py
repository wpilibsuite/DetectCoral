#!/usr/bin/env python2.7

import os, shutil, fileinput, tarfile, subprocess
import labels, sed, modularized_model_main, tar_to_record
from os.path import join

def main():

    TRAIN_STEPS = 1000
    BATCH_SIZE = 32
    outputdir = '/opt/ml/model/'

    tar_to_record.main(outputdir, '/opt/ml/input/data/training/')

    classes = labels.get()
    sed.replace_words('NUM_CLASSES', str(classes), "pipeline.config")
    sed.replace_words('BATCH_SIZE_PARAM', str(BATCH_SIZE), "pipeline.config")

    shutil.copy('pipeline.config','learn/ckpt/pipeline.config')
    shutil.rmtree('learn/train', ignore_errors=True)
    os.mkdir('learn/train')

    modularized_model_main.main(
        pipeline_config_path='learn/ckpt/pipeline.config',
        model_dir='learn/train',
        num_train_steps=TRAIN_STEPS)

    # here we should write the class tags of
    # /opt/ml/input/data/training/Raw Data/meta.json to a labelmap file.
    with open('labels.txt', 'w') as labelfile:
        labelfile.writelines(['0 powercell'])

    print('\nconverting checkpoint to tflite')
    subprocess.check_call("./convert_checkpoint_to_edgetpu_tflite.sh --checkpoint_num %s" % (str(TRAIN_STEPS)),
                          shell=True)
    shutil.copy('learn/models/output_tflite_graph.tflite', join(outputdir,'unoptimized.tflite'))

    print('\ncompiling model for edge TPU')
    subprocess.check_call("edgetpu_compiler ./learn/models/output_tflite_graph.tflite -o %s"%(outputdir), shell=True)

    with tarfile.open(join(outputdir,'model.tar.gz'),'w:gz') as model:
        model.add(join(outputdir,'output_tflite_graph_edgetpu.tflite'),arcname='model.tflite')
        model.add('/opt/ml/input/data/training/map.pbtxt',arcname='map.pbtxt')
        model.add(join(outputdir,'unoptimized.tflite'),arcname='unoptimized.tflite')

    print('All done.')


if __name__ == "__main__":
    main()
