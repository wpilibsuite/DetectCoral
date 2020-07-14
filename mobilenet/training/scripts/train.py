#!/usr/bin/env python2.7
import matplotlib as mpl

mpl.use('Agg')
import os, shutil, subprocess
import labels, sed, modularized_model_main, parse_hyperparams, prepare_checkpoint

OUTPUT_PATH = '/opt/ml/model/finished-models'
train_path = '/opt/ml/model/train'


def logstatus(message):
    print(message)
    with open('status.txt', 'w') as status:
        status.write(message)


def main():
    data = parse_hyperparams.parse("/opt/ml/model/hyperparameters.json")
    # todo: use model type
    TRAIN_STEPS = data["epochs"]
    BATCH_SIZE = data["batch-size"]
    EVAL_FREQ = data["eval-frequency"]
    CHECKPOINT = data["checkpoint"]

    shutil.rmtree(train_path, ignore_errors=True)
    os.mkdir(train_path)

    prepare_checkpoint.prepare_checkpoint(None)

    with open('pipeline.config') as config:
        config = config.read()
        if '/tensorflow/models/research/learn/ckpt/%s/model.ckpt' % (CHECKPOINT) not in config:
            sed.replace_words(
                '/tensorflow/models/research/learn/ckpt/ssd_mobilenet_v2_quantized_300x300_coco_2019_01_03/model.ckpt',
                '/tensorflow/models/research/learn/ckpt/%s/model.ckpt' % (CHECKPOINT), "pipeline.config")

    classes = labels.get()
    sed.replace_words('NUM_CLASSES', str(classes), "pipeline.config")
    sed.replace_words('BATCH_SIZE_PARAM', str(BATCH_SIZE), "pipeline.config")
    shutil.copy('pipeline.config', '/opt/ml/model/pipeline.config')

    subprocess.Popen(['tensorboard', '--logdir', 'learn/train'])

    logstatus('training the model')
    modularized_model_main.main(
        pipeline_config_path='/opt/ml/model/pipeline.config',
        model_dir=train_path,
        num_train_steps=TRAIN_STEPS,
        eval_period=EVAL_FREQ)


if __name__ == "__main__":
    main()
