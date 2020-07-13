import sys, os, shutil, tarfile
import json_to_csv, generate_tfrecord, parse_meta, parse_hyperparams
from os.path import join


def main(dataset_path, output_path, percent_eval):
    try:
        shutil.copy(dataset_path, join(output_path, 'data.tar'))
    except:
        print('unable to retrieve the dataset tar file.')
        sys.exit(1)

    with tarfile.open(join(output_path, 'data.tar')) as tar_file:
        tar_file.extractall(join(output_path, 'out'))

    if percent_eval > 100 or percent_eval < 100:
        percent_eval = 30
    json_to_csv.main(percent_eval)

    generate_tfrecord.main(join(output_path, 'tmp/train.csv'), join(output_path, 'train.record'))
    generate_tfrecord.main(join(output_path, 'tmp/eval.csv'), join(output_path, 'eval.record'))

    parse_meta.main(join(output_path, 'map.pbtxt'))

    print(".\nRecords generated")


if __name__ == "__main__":
    data = parse_hyperparams.parse("/opt/ml/model/hyperparameters.json")
    DATASET_PATH = data["dataset-path"]
    PERCENT_EVAL = data["percent-eval"]
    main(DATASET_PATH, '/opt/ml/model', PERCENT_EVAL)
