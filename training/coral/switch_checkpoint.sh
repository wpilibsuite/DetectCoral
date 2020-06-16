#!/bin/bash
set -e
source "$PWD/constants.sh"

if [ $# -eq 1 ]
then
    network_type=$1
else
    echo "Please give the name of the pre-trained model you would like to use."
    exit 1
fi

rm -rf learn
mkdir -p learn/ckpt
rm -rf learn/train
rm -rf learn/models

ckpt_link="${ckpt_link_map[${network_type}]}"
ckpt_name="${ckpt_name_map[${network_type}]}"
echo switching pretrained model to $ckpt_name
wget -q -O "${ckpt_name}.tar.gz" "$ckpt_link"
python prepare_checkpoint.py --network_type ${network_type}
