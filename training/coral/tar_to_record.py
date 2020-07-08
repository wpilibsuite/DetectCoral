import sys, os, glob, shutil, tarfile
import json_to_csv, generate_tfrecord, parse_meta
from os.path import join


def main(datasetpath, outputpath):
    shutil.rmtree(join(outputpath, 'out'), ignore_errors=True)
    shutil.rmtree(join(outputpath, 'tmp'), ignore_errors=True)
    os.mkdir(join(outputpath, 'out'))
    os.mkdir(join(outputpath, 'tmp'))

    print(datasetpath)

    try:
        shutil.copy(datasetpath, join(outputpath, 'data.tar'))
    except:
        print('unable to retrieve the dataset tar file.')
        sys.exit(1)

    with tarfile.open(join(outputpath, 'data.tar')) as tar_file:
        tar_file.extractall(join(outputpath, 'out'))

    json_to_csv.main()

    generate_tfrecord.main(join(outputpath, 'tmp/train.csv'), join(outputpath, 'train.record'))

    generate_tfrecord.main(join(outputpath, 'tmp/eval.csv'), join(outputpath, 'eval.record'))

    parse_meta.main(join(outputpath, 'map.pbtxt'))

    print(".\nRecords generated")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--datasetdir',
                        help='This is the path to the directory where you will put you desired dataset before training. It should be alone.',
                        type=str, required=True)
    parser.add_argument('-o', '--outputdir',
                        help='This is the path to the directory that the records will go. It should only be /opt/ml/input/data/training right now.',
                        type=str, required=True)
    args = parser.parse_args()

    main(args.datasetdir, args.outputdir)
