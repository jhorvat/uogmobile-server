FROM frolvlad/alpine-python3:latest
ADD . /opt/webapp/
WORKDIR /opt/webapp

RUN pip install -r requirements.txt
CMD python3 runner.py
