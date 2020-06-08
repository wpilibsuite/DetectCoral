DIR=${PWD}
echo ${DIR}
docker run --name wpi \
       --rm -it -p 80:8080 \
       --mount type=bind,src=${DIR},dst=/opt/ml/model \
       wpi-cpu-local
