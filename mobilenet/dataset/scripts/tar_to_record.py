import sys, os, shutil, tarfile
import json_to_csv, generate_tfrecord, parse_meta, parse_hyperparams
from os.path import join


def main(dataset_path, percent_eval):
    OUTPUT_PATH = "/opt/ml/model"
    EXTRACT_PATH = "/home"
    TMP_PATH = "/home/tmp"

    if not os.path.exists(TMP_PATH):
        os.makedirs(TMP_PATH)
    if not os.path.exists(EXTRACT_PATH):
        os.makedirs(EXTRACT_PATH)

    try:
        shutil.copy(dataset_path, join(EXTRACT_PATH, 'data.tar'))
    except:
        print('unable to retrieve the dataset tar file.')
        sys.exit(1)
    with tarfile.open(join(EXTRACT_PATH, 'data.tar')) as tar_file:
        tar_file.extractall(join(EXTRACT_PATH, 'out'))

    if percent_eval > 100 or percent_eval < 100:
        percent_eval = 30
    json_to_csv.main(percent_eval)

    generate_tfrecord.main(TMP_PATH + "/train.csv", join(OUTPUT_PATH, 'train.record'))
    generate_tfrecord.main(TMP_PATH + "/eval.csv", join(OUTPUT_PATH, 'eval.record'))

    parse_meta.main(join(OUTPUT_PATH, 'map.pbtxt'))

    print(".\nRecords generated")


if __name__ == "__main__":
    data = parse_hyperparams.parse("/opt/ml/model/hyperparameters.json")
    DATASET_PATH = data["dataset-path"]
    PERCENT_EVAL = data["percent-eval"]
    main(DATASET_PATH, PERCENT_EVAL)
