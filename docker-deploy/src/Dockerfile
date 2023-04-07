FROM ubuntu:20.04
RUN apt-get update && apt-get install libpq-dev python-dev python3-pip -y
RUN mkdir newRoot
WORKDIR /newRoot
ADD . /newRoot
RUN pip3 install -r /newRoot/requirements.txt
RUN chmod +x runserver.sh
