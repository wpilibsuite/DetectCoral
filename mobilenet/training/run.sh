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
cp ../dataset/mount/eval.record ./mount/eval.record
cp ../dataset/mount/train.record ./mount/train.record
cp ../dataset/mount/map.pbtxt ./mount/map.pbtxt

docker rm train
docker run --gpus all --name train \
       -p 5000:5000 -p 6006:6006\
       --mount type=bind,src=${DIR},dst=/opt/ml/model \
       gcperkins/wpilib-ml-train:latest
# --entrypoint "/bin/bash" -it