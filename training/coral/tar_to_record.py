import sys, os, glob, shutil, tarfile
import json_to_csv, generate_tfrecord, parse_meta
from os.path import join

if __name__ == "__main__":
    outputpath = '/opt/ml/input/data/training'
    shutil.rmtree(join(outputpath,'out'), ignore_errors=True)
    shutil.rmtree(join(outputpath,'tmp'), ignore_errors=True)
    os.mkdir(join(outputpath,'out'))
    os.mkdir(join(outputpath,'tmp'))

    tar_file = glob.glob(join(outputpath,"*.tar"))[0]
    shutil.copy(tar_file, join(outputpath,'data.tar'))
    print(tar_file)

    with tarfile.open(join(outputpath,'data.tar')) as tar_file:
        tar_file.extractall(join(outputpath,'out'))

    json_to_csv.main()

    generate_tfrecord.main(join(outputpath,'tmp/train.csv'), join(outputpath,'train.record'))

    generate_tfrecord.main(join(outputpath,'tmp/eval.csv'), join(outputpath,'eval.record'))

    parse_meta.main(join(outputpath,'map.pbtxt'))

    print(".\nRecords generated")
