#!/bin/bash

usage() {
  cat << END_OF_USAGE
  Install dependencies for inference on a Raspberry Pi.
  
  --input -i         Path of model.tar.gz downloaded from SageMaker
  --help            Print this help.
END_OF_USAGE
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    -i | --input)
      path=$2
      shift 2 ;;
    -h | --help)
      usage
      exit 0 ;;
    --*)
      echo "Unknown flag $1"
      usage
      exit 1 ;;
  esac
done


echo "Extracting $path"
tar zxvf $path
