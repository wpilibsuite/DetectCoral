DIR=$PWD/mount
while [[ $# -gt 0 ]]; do
  case "$1" in
    --mount)
      DIR=$DIR/$2
      shift 2 ;;
    --*)
      echo "Unknown flag $1"
      exit 1 ;;
  esac
done

mkdir -p $DIR
cp ../../hyperparameters.json ./mount/hyperparameters.json
cp -R ../training/mount/train/ ./mount/train/
cp ../dataset/mount/map.pbtxt ./mount/map.pbtxt
cp ../training/mount/pipeline.config ./mount/pipeline.config
docker rm tflite
docker run --name tflite \
       --mount type=bind,src=${DIR},dst=/opt/ml/model \
       gcperkins/wpilib-ml-tflite:latest
# --entrypoint "/bin/bash" -it