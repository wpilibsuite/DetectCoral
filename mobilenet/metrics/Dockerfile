FROM gcperkins/wpilib-ml-base:small

COPY scripts /tensorflow/models/research/
WORKDIR /tensorflow/models/research/
ENTRYPOINT ["python"]
CMD ["output_metrics.py"]