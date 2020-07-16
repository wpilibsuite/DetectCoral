#!/usr/bin/env python2.7
import os
import shutil
import subprocess

import labels
import modularized_model_main
import parse_hyperparams
import sed

OUTPUT_PATH = '/opt/ml/model/finished-models'
TRAIN_PATH = '/opt/ml/model/train'


def main():
    data = parse_hyperparams.parse("/opt/ml/model/hyperparameters.json")
    TRAIN_STEPS = data["epochs"]
    BATCH_SIZE = data["batch-size"]
    EVAL_FREQ = data["eval-frequency"]
    CHECKPOINT = data["checkpoint"]

    shutil.rmtree(TRAIN_PATH, ignore_errors=True)
    os.mkdir(TRAIN_PATH)

    if CHECKPOINT != "default":
        sed.replace_words(
            '/tensorflow/models/research/start_ckpt/model.ckpt',
            '/opt/ml/model/train/model.ckpt-%s' % (CHECKPOINT), "pipeline.config")

    classes = labels.get()
    sed.replace_words('NUM_CLASSES', str(classes), "pipeline.config")
    sed.replace_words('BATCH_SIZE_PARAM', str(BATCH_SIZE), "pipeline.config")

    subprocess.Popen(['tensorboard', '--logdir', 'learn/train'])
    shutil.copy('pipeline.config', '/opt/ml/model/pipeline.config')

    modularized_model_main.main(
        pipeline_config_path='pipeline.config',
        model_dir=TRAIN_PATH,
        num_train_steps=TRAIN_STEPS,
        eval_period=EVAL_FREQ)



if __name__ == "__main__":
    main()
