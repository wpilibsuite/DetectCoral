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
echo ${DIR}

mkdir -p $DIR
docker run --entrypoint "/bin/bash" --name wpi \
       -it -p 5000:5000 \
       --mount type=bind,src=${DIR},dst=/opt/ml/model \
       wpi-cpu-local
