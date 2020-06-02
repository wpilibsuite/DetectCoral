FROM tensorflow/tensorflow:1.12.0-rc2-devel

ARG DEBIAN_FRONTEND=noninteractive

RUN cd / & mkdir tensorflow
# Get the tensorflow models research directory, and move it into tensorflow
# source folder to match recommendation of installation
RUN git clone https://github.com/tensorflow/models.git && \
    (cd models && git checkout f788046ca876a8820e05b0b48c1fc2e16b0955bc) && \
    mv models /tensorflow/models
    
RUN apt-get update && apt-get install -y --no-install-recommends nginx curl
RUN apt-get install wget

RUN mkdir -p /opt/ml/input/data/training && \
 mkdir -p /opt/ml/model/ && \
cd /opt/ml/input/data/training && \
wget https://github.com/GrantPerkins/DetectCoral/releases/download/v1.0.1/RawData.tar -q

RUN mkdir -p /opt/ml/input/config/


# Install the Tensorflow Object Detection API from here
# https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/installation.md

# Install object detection api dependencies
RUN apt-get update && \
    apt-get install -y python python-tk
RUN pip install Cython && \
    pip install contextlib2 && \
    pip install pillow && \
    pip install lxml && \
    pip install jupyter && \
    pip install matplotlib
RUN cd /
# Get protoc 3.0.0, rather than the old version already in the container
RUN curl -OL "https://github.com/google/protobuf/releases/download/v3.0.0/protoc-3.0.0-linux-x86_64.zip" && \
    unzip protoc-3.0.0-linux-x86_64.zip -d proto3 && \
    mv proto3/bin/* /usr/local/bin && \
    mv proto3/include/* /usr/local/include && \
    rm -rf proto3 protoc-3.0.0-linux-x86_64.zip

# Install pycocoapi
RUN git clone --depth 1 https://github.com/cocodataset/cocoapi.git && \
    cd cocoapi/PythonAPI && \
    make -j8 && \
    cp -r pycocotools /tensorflow/models/research && \
    cd ../../ && \
    rm -rf cocoapi

# Run protoc on the object detection repo
RUN cd /tensorflow/models/research && \
    protoc object_detection/protos/*.proto --python_out=.

# Set the PYTHONPATH to finish installing the API
ENV PYTHONPATH $PYTHONPATH:/tensorflow/models/research:/tensorflow/models/research/slim

# Install wget (to make life easier below) and editors (to allow people to edit
# the files inside the container)
RUN apt-get update && \
    apt-get install -y wget vim emacs nano

RUN apt-get install -y apt-transport-https ca-certificates

ARG work_dir=/tensorflow/models/research
# Get object detection transfer learning scripts.
ARG scripts_link="http://storage.googleapis.com/cloud-iot-edge-pretrained-models/docker/obj_det_scripts.tgz"

RUN cd ${work_dir} && \
    wget -O obj_det_scripts.tgz ${scripts_link} && \
    tar zxvf obj_det_scripts.tgz

RUN curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add - && \
    echo "deb https://packages.cloud.google.com/apt coral-edgetpu-stable main" | tee /etc/apt/sources.list.d/coral-edgetpu.list && \
    apt-get update && \
    apt-get install edgetpu-compiler -y

ENV PATH="/tensorflow/models/research:${PATH}"
# Copy WPILib scripts into docker image
COPY /coral /tensorflow/models/research

RUN cd /tensorflow/models/research && mv hyperparameters.json /opt/ml/input/config/hyperparameters.json

WORKDIR /tensorflow/models/research
