from jjanzic/docker-python3-opencv

RUN mkdir work

ARG work_dir=/work

RUN apt-get update -qq > /dev/null && \
    apt-get install -y python python-tk python3 python3-pip -qq > /dev/null
    
RUN apt-get update -qq > /dev/null && \
    apt-get install -y wget vim emacs nano -qq > /dev/null
    
RUN apt-get install -y apt-transport-https ca-certificates

RUN apt-get update && apt-get -y install cmake protobuf-compiler

#RUN wget https://dl.google.com/coral/python/tflite_runtime-1.14.0-cp35-cp35m-linux_x86_64.whl && \
#    pip3 install tflite_runtime-1.14.0-cp35-cp35m-linux_x86_64.whl
    
RUN pip3 install tensorflow

COPY /coral /work

# Add train to path for SageMaker to find
ENV PATH $PATH:/work

WORKDIR ${work_dir}