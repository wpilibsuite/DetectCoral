FROM borda/docker_python-opencv-ffmpeg


RUN mkdir -p /tensorflow/models/research/ && \
    cd /tensorflow/models/research/ && \
    apt-get update && \
    apt-get install wget -y && \
    python3 --version && \
    wget "https://github.com/wpilibsuite/DetectCoral/releases/download/v2/testing.mp4" --no-check-certificate

RUN pip3 install pillow && \
    pip3 install https://github.com/google-coral/pycoral/releases/download/release-frogfish/tflite_runtime-2.5.0-cp37-cp37m-linux_x86_64.whl

COPY scripts /tensorflow/models/research/
WORKDIR /tensorflow/models/research/
CMD ["python3", "-u", "test.py"]