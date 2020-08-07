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
cp ../../params/testparameters.json ./mount/testparameters.json
cp ../tflite/mount/model.tar.gz ./mount/model.tar.gz
cp ../dataset/mount/map.pbtxt ./mount/map.pbtxt

docker rm test
docker run --name test \
        -p 5000:5000 \
        --mount type=bind,src=${DIR},dst=/opt/ml/model \
        gcperkins/wpilib-ml-test:latest
# --entrypoint "/bin/bash" -it
