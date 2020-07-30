DIR=$PWD/../training/mount
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

docker rm metrics
docker run --name metrics \
      -p 6006:6006 \
       --mount type=bind,src=${DIR},dst=/opt/ml/model \
       gcperkins/wpilib-ml-metrics:latest
# --entrypoint "/bin/bash" -it