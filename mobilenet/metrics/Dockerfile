FROM gcperkins/wpilib-ml-base

COPY scripts /tensorflow/models/research/
WORKDIR /tensorflow/models/research/
ENTRYPOINT ["python"]
CMD ["output_metrics.py"]