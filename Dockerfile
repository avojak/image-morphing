FROM python:3.8-slim

COPY ./lib ./lib
COPY ./web ./web
COPY ./requirements.txt .

RUN apt-get update && \
    apt-get install -y libglib2.0-0 \
                       libsm6 \
                       libxext6 \
                       libxrender-dev \
                       imagemagick && \
    pip install -r requirements.txt && \
    pip install ./lib/ && \
    pip install ./web/

EXPOSE 8080

ENTRYPOINT waitress-serve --call 'webmorphing:create_app'