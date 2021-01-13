# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:2.7.17

RUN pip uninstall -y enum34
RUN pip install --upgrade pip enum34
RUN pip install --upgrade google-cloud-storage
COPY . ./
RUN pip install -r requirements.txt
RUN apt install git
RUN git submodule init
RUN git submodule 