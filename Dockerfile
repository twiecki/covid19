FROM tensorflow/tensorflow:2.0.1-gpu-py3-jupyter

LABEL maintainer="Fabio Nonato (@nonatofabio)"

ADD requirements.txt /

ADD startup.sh /

RUN pip install -r /requirements.txt

CMD ["./startup.sh"]
