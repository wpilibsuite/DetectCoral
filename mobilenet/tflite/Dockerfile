FROM gcperkins/wpilib-ml-base

ENV OPENCV_VERSION="3.4.1"
RUN set -e -x && \
    cd / && \
    wget https://github.com/opencv/opencv/archive/${OPENCV_VERSION}.zip && \
    unzip ${OPENCV_VERSION}.zip && \
    mkdir /opencv-${OPENCV_VERSION}/cmake_binary && \
    cd /opencv-${OPENCV_VERSION}/cmake_binary && \
    cmake -DBUILD_TIFF=ON \
        -DBUILD_opencv_java=OFF \
        -DWITH_CUDA=OFF \
        -DENABLE_AVX=ON \
        -DWITH_OPENGL=ON \
        -DWITH_OPENCL=ON \
        -DWITH_IPP=ON \
        -DWITH_TBB=ON \
        -DWITH_EIGEN=ON \
        -DWITH_V4L=ON \
        -DBUILD_TESTS=OFF \
        -DBUILD_PERF_TESTS=OFF \
        -DCMAKE_BUILD_TYPE=RELEASE \
        -DCMAKE_INSTALL_PREFIX=$(python -c "import sys; print sys.prefix ") \
        -DPYTHON_EXECUTABLE=$(which python) \
        -DPYTHON_INCLUDE_DIR=$(python -c "from distutils.sysconfig import get_python_inc; print get_python_inc()") \
        -DPYTHON_PACKAGES_PATH=$(python -c "from distutils.sysconfig import get_python_lib; print get_python_lib()") .. && \
    make install && \
    rm /${OPENCV_VERSION}.zip && \
    rm -r /opencv-${OPENCV_VERSION}

RUN curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add - && \
    echo "deb https://packages.cloud.google.com/apt coral-edgetpu-stable main" | tee /etc/apt/sources.list.d/coral-edgetpu.list && \
    apt-get update && \
    apt-get install edgetpu-compiler -y && \
    mkdir -p /tensorflow/models/research/learn && \
    mkdir -p /tensorflow/models/research/learn/ckpt && \
    mkdir -p /opt/ml/model/checkpoints/ && \
    rm -rf /tensorflow/models/research/learn/train && \
    rm -rf /tensorflow/models/research/learn/models && \
    cd /tensorflow/models/research/ && \
    pip install pillow && \
    wget "https://github.com/wpilibsuite/DetectCoral/releases/download/v2/tflite_graph.pb" && \
    wget "https://github.com/wpilibsuite/DetectCoral/releases/download/v2/testing.mp4"

COPY scripts /tensorflow/models/research/
WORKDIR /tensorflow/models/research/
CMD ["python", "-u", "export.py"]