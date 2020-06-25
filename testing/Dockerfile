from jjanzic/docker-python3-opencv

ARG DEBIAN_FRONTEND=noninteractive

RUN pwd
RUN mkdir work

ARG work_dir=/work

RUN mkdir -p /opt/ml/input/data/training && \
 mkdir  -p /opt/ml/model/ && \
 mkdir  -p /opt/ml/input/data/model

RUN apt-get update -qq > /dev/null && \
    apt-get install -y python python-tk python3 python3-pip -qq > /dev/null
    
RUN apt-get update -qq > /dev/null && \
    apt-get install -y wget vim emacs nano -qq > /dev/null
    
RUN apt-get install -y apt-transport-https ca-certificates

RUN apt-get update && apt-get -y install cmake protobuf-compiler

#RUN wget https://dl.google.com/coral/python/tflite_runtime-1.14.0-cp35-cp35m-linux_x86_64.whl && \
#    pip3 install tflite_runtime-1.14.0-cp35-cp35m-linux_x86_64.whl
    
RUN pip3 install tensorflow

RUN cd /opt/ml/input/data/training && \
wget https://github.com/GrantPerkins/DetectCoral/releases/download/v1.0.2/Kevin-stitched-video.mp4

COPY /coral /work

# Add train to path for SageMaker to find
ENV PATH $PATH:/work

WORKDIR ${work_dir}

RUN echo "done building"
