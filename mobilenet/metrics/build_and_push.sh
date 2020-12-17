name=wpilib-ml-metrics

name_with_tag="gcperkins/${name}:small"

docker build  -t ${name} .
docker tag ${name} ${name_with_tag}
docker push ${name_with_tag}