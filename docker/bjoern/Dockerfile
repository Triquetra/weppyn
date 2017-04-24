FROM alpine:latest

# Install python
RUN apk update && apk upgrade && \
	apk add --no-cache python py2-pip && \
	pip install -U --no-cache-dir pip setuptools

# Install build dependencies and test suite dependencies
RUN apk add --no-cache --virtual build-deps gcc musl-dev python-dev libev-dev
RUN pip install -U --no-cache-dir pytest ipdb delegator.py requests
RUN pip install -U --no-cache-dir weppy
RUN apk add --no-cache libev
RUN pip install -U --no-cache-dir bjoern

# Remove build dependencies
RUN apk del build-deps

# Install weppyn
COPY . /tmp/weppyn/
RUN	pip install --no-cache-dir /tmp/weppyn

COPY ./tests/commands/sample_app.py /home/weppy/

EXPOSE 8000

CMD ["pytest", "/tmp/weppyn/"]