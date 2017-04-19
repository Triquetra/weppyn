FROM alpine:latest

# Install python 3, pulsar wsgi server, and weppy
RUN apk update && apk upgrade && \
	apk add --no-cache python3 && ln -s /usr/bin/python3 /usr/bin/python && \
	pip3 install -U --no-cache-dir pip setuptools

# Install test suite dependencies
RUN pip3 install -U --no-cache-dir pytest pytest-cov ipdb delegator.py requests

# Install build dependencies
RUN pip3 install -U --no-cache-dir weppy
RUN apk add --no-cache --virtual build-deps gcc musl-dev python3-dev make
RUN pip3 install -U --no-cache-dir meinheld

# Remove build dependencies
RUN apk del build-deps

# Install weppyn
COPY . /tmp/weppyn/
RUN	pip3 install --no-cache-dir /tmp/weppyn

COPY ./tests/commands/sample_app.py /home/weppy/

EXPOSE 8000

# ENTRYPOINT ["python", "/tmp/weppyn/docker/entrypoint.py"]

# CMD ["run", "meinheld"]