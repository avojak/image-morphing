FROM python:3.8-slim

COPY ./lib/dist/libmorphing-*.tar.gz .
COPY ./web/dist/webmorphing-*.tar.gz .
COPY ./requirements.txt .

RUN apt-get update && \
    apt-get install -y libglib2.0-0 \
                       libsm6 \
                       libxext6 \
                       libxrender-dev \
                       imagemagick && \
    pip install -r requirements.txt && \
    pip install ./libmorphing-*.tar.gz \
                ./webmorphing-*.tar.gz && \
    rm ./requirements.txt \
       ./libmorphing-*.tar.gz \
       ./webmorphing-*.tar.gz

EXPOSE 8080

ENTRYPOINT waitress-serve --call 'webmorphing:create_app'