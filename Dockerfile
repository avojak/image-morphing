FROM python:3.8-slim

COPY ./lib/dist/libmorphing-*.tar.gz .
COPY ./web/dist/webmorphing-*.tar.gz .
COPY ./requirements.txt .

RUN pip install -r requirements.txt && \
    pip install ./libmorphing-*.tar.gz && \
    pip install ./webmorphing-*.tar.gz && \
    rm ./requirements.txt && \
    rm ./libmorphing-*.tar.gz && \
    rm ./webmorphing-*.tar.gz

EXPOSE 8080

ENTRYPOINT waitress-serve --call 'webmorphing:create_app'