FROM gcperkins/wpilib-ml-base:small

RUN mkdir -p /opt/ml/model/tmp && \
    mkdir -p /opt/ml/model/out && \
    pip install pandas
COPY scripts /tensorflow/models/research/

WORKDIR /tensorflow/models/research/
ENTRYPOINT ["python"]
CMD ["tar_to_record.py"]