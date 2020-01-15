FROM python:3.7-alpine

ENV TELEGRAM_API_TOKEN="889544738:AAFK2hC2-YPApaHp0DpkZdUY1WBLkp6XpMs"
ENV TELEGRAM_ACCESS_ID="176082570"
ENV TELEGRAM_PROXY_URL=""
ENV TELEGRAM_PROXY_LOGIN=""
ENV TELEGRAM_PROXY_PASSWORD=""

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

ENTRYPOINT ["python", "main.py"]
