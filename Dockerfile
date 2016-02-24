FROM frolvlad/alpine-python3:latest

ADD ./requirements.txt /tmp/requirements.txt
RUN pip install -qr /tmp/requirements.txt
ADD . /opt/webapp/

WORKDIR /opt/webapp
EXPOSE 5000
CMD ["python3", "run.py"]
