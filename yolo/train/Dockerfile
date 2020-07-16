FROM gcperkins/yolo-base:latest
RUN cd /home/ && \
    git clone https://github.com/pjreddie/darknet.git && \
    cd darknet && \
    make
RUN mkdir -p /yolo/
COPY scripts /yolo/