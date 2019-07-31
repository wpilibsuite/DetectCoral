#!/bin/bash

cd /opt/ml/input/data/training
rm -rf out
mkdir out
mkdir tmp
tar_file=$(find . -name *.tar*)

tar -xf $tar_file -C ./out/

python3 /tensorflow/models/research/json_to_csv.py

python /tensorflow/models/research/generate_tfrecord.py --input_csv=./tmp/train.csv --output_tfrecord=train.record

python /tensorflow/models/research/generate_tfrecord.py --input_csv=./tmp/eval.csv --output_tfrecord=eval.record

python3 /tensorflow/models/research/parse_meta.py -out=map.pbtxt

echo "Records generated."