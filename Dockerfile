FROM python:3.7-alpine

RUN apk update && apk upgrade
RUN apk add --no-cache bash\
                       python \
                       pkgconfig \
                       git \
                       gcc \
                       openldap \
                       libcurl \
                       python2-dev \
                       gpgme-dev \
                       libc-dev \
    && rm -rf /var/cache/apk/*

COPY src/ /home/root
WORKDIR /home/root

RUN pip install -r requirements.txt

CMD ["python", "main.py"]
