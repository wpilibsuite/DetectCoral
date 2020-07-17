#!/usr/bin/env python2.7
import os
import shutil
import subprocess

import labels
import modularized_model_main
import parse_hyperparams
import sed
from log_parser import EvalJSONifier

def main():
    TRAIN_PATH = '/opt/ml/model/train'
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

    subprocess.Popen(['tensorboard', '--logdir', '/opt/ml/model/train'])
    shutil.copy('pipeline.config', '/opt/ml/model/pipeline.config')

    json_thread = EvalJSONifier(TRAIN_STEPS)
    json_thread.start()
    print("Starting training.")
    modularized_model_main.main(
        pipeline_config_path='pipeline.config',
        model_dir=TRAIN_PATH,
        num_train_steps=TRAIN_STEPS,
        eval_period=EVAL_FREQ)
    print("training done.")
    json_thread.join()
    print("Thread joined.")

if __name__ == "__main__":
    print("sanity check")
    main()
