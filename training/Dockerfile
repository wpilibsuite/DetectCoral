FROM tensorflow/tensorflow:1.12.0-rc2-devel

ARG DEBIAN_FRONTEND=noninteractive

RUN cd / & mkdir tensorflow && \
    git clone https://github.com/tensorflow/models.git && \
    (cd models && git checkout f788046ca876a8820e05b0b48c1fc2e16b0955bc) && \
    mv models /tensorflow/models
    
RUN apt-get update && \
    apt-get install -y --no-install-recommends nginx curl wget python python-tk apt-transport-https ca-certificates && \
    pip install Cython && \
    pip install contextlib2 && \
    pip install pillow && \
    pip install matplotlib && \
    mkdir -p /opt/ml/input/data/training && \
    mkdir -p /opt/ml/model/ && \
    cd /opt/ml/input/data/training && \
    wget https://github.com/GrantPerkins/DetectCoral/releases/download/v1.0.2/full_data.tar -q

# RUN mkdir -p /opt/ml/input/config/

# Get protoc 3.0.0, rather than the old version already in the container
RUN cd / && \
    curl -OL "https://github.com/google/protobuf/releases/download/v3.0.0/protoc-3.0.0-linux-x86_64.zip" && \
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
    rm -rf cocoapi && \
    cd /tensorflow/models/research && \
    protoc object_detection/protos/*.proto --python_out=.

# Set the PYTHONPATH to finish installing the API
ENV PYTHONPATH $PYTHONPATH:/tensorflow/models/research:/tensorflow/models/research/slim

RUN cd /tensorflow/models/research && \
    wget -O "obj_det_scripts.tgz" "http://storage.googleapis.com/cloud-iot-edge-pretrained-models/docker/obj_det_scripts.tgz" && \
    tar zxvf obj_det_scripts.tgz

RUN curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add - && \
    echo "deb https://packages.cloud.google.com/apt coral-edgetpu-stable main" | tee /etc/apt/sources.list.d/coral-edgetpu.list && \
    apt-get update && \
    apt-get install edgetpu-compiler -y && \
    RUN mkdir -p /tensorflow/models/research/learn && \
    mkdir -p /tensorflow/models/research/learn/ckpt && \
    rm -rf /tensorflow/models/research/learn/train && \
    rm -rf /tensorflow/models/research/learn/models && \
    cd /tensorflow/models/research && \
    wget -q -O "ssd_mobilenet_v2_quantized_300x300_coco_2019_01_03.tar.gz" "http://download.tensorflow.org/models/object_detection/ssd_mobilenet_v2_quantized_300x300_coco_2019_01_03.tar.gz"

ENV PATH="/tensorflow/models/research:${PATH}"
# Copy WPILib scripts into docker image
COPY /coral /tensorflow/models/research

RUN cd /tensorflow/models/research && \
    python prepare_checkpoint.py --network_type mobilenet_v2_ssd

WORKDIR /tensorflow/models/research/
ENTRYPOINT ["python"]
CMD ["train.py"]