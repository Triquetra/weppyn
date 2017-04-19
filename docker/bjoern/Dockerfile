FROM alpine:latest

# Install python, pulsar wsgi server, and weppy
RUN apk update && apk upgrade && \
	apk add --no-cache python3 && ln -s /usr/bin/python3 /usr/bin/python && \
	apk add --no-cache --virtual build-deps gcc musl-dev python3-dev make && \
    pip3 install -U --no-cache-dir pip setuptools wheel && \
    pip3 install -U --no-cache-dir pulsar uvloop http-parser weppy && \
    apk del build-deps

RUN mkdir /home/weppy
COPY ./weppy/* /home/weppy
RUN chmod +x /home/weppy/myapp.py

EXPOSE 8000

CMD ["/home/weppy/myapp.py"]