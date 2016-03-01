# FROM debian:latest
FROM monsantoco/min-jessie:latest

RUN apt-get update \
    && apt-get upgrade -qqy \
    && apt-get install -qqy --no-install-recommends \
        build-essential g++ flex bison gperf ruby perl \
        libsqlite3-dev libfontconfig1-dev libicu-dev libfreetype6 libssl-dev \
        libpng-dev libjpeg-dev python libx11-dev libxext-dev git \
    && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/jhorvat/phantomjs.git /tmp/phantomjs
WORKDIR /tmp/phantomjs

RUN git checkout selenium-hub-fix && \
    git submodule init && \
    git submodule update && \
    python build.py && \
    chmod +x bin/phantomjs && \
    cp bin/phantomjs /opt/phantomjs

WORKDIR /opt
RUN rm -rf /tmp/phantomjs

CMD ./phantomjs --webdriver=5555 --webdriver-selenium-grid-hub=http://hub:4444/ --load-images=false
