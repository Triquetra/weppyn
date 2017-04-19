FROM alpine:latest

# Install python 3, pulsar wsgi server, and weppy
RUN apk update && apk upgrade && \
	apk add --no-cache python3 && ln -s /usr/bin/python3 /usr/bin/python && \
	pip3 install -U --no-cache-dir pip setuptools wheel

# Install build dependencies for uvloop, and http-parser
RUN apk add --no-cache --virtual build-deps gcc musl-dev python3-dev make

# Install pulsar and plugins
RUN pip3 install -U --no-cache-dir pulsar uvloop http-parser greenlet

# Install weppyn and test packages
RUN pip3 install -U --no-cache-dir pytest ipdb && \
	pip3 install -U --no-cache-dir ./src/weppyn && \
	mkdir /home/weppy

COPY ./tests/commands/sample_app.py /home/weppy/

# Remove build dependencies
RUN apk del build-deps

EXPOSE 8060

ENTRYPOINT ["weppyn", "pulsar"]

CMD ["/home/weppy/sample_app.py", "--bind", "0.0.0.0"]