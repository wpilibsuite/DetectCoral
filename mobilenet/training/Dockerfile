FROM gcperkins/wpilib-ml-base

COPY scripts /tensorflow/models/research/

RUN mkdir -p /tensorflow/models/research/learn && \
    mkdir -p /tensorflow/models/research/learn/ckpt && \
    rm -rf /tensorflow/models/research/learn/train && \
    rm -rf /tensorflow/models/research/learn/models && \
    cd /tensorflow/models/research
WORKDIR /tensorflow/models/research/
ENTRYPOINT ["python"]
CMD ["train.py"]