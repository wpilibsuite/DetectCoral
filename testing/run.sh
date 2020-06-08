DIR=${PWD}
echo ${DIR}
docker run --name wpi2 \
       --rm -it -p 6006:6006 \
       --mount type=bind,src=${DIR},dst=/opt/ml/model \
       wpi-test-local bash
