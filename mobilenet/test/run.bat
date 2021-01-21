docker build --no-cache -t wpilib/axon-test:edge .
docker kill test
docker rm test
docker run --name test -p 5000:5000 --mount type=bind,src=C:\Users\gcper\Code\Work\DetectCoral\mobilenet\test\mount,dst=/opt/ml/model wpilib/axon-test:edge
