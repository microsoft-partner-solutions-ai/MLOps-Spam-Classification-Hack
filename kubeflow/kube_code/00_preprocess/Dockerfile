FROM mcr.microsoft.com/azureml/openmpi3.1.2-ubuntu18.04:20210615.v1

# pip install
COPY requirements.txt /scripts/requirements.txt
RUN set -xe \
    && apt-get update -y \
    && apt-get install -y python3-pip
RUN pip install --upgrade pip
RUN pip install -r /scripts/requirements.txt

COPY PrepareTrainingData.py /scripts/PrepareTrainingData.py
# Can I copy an entire data folder?
COPY ./data/ /data/

# will be overwritten by kf pipeline
ENTRYPOINT [ "python", "/scripts/PrepareTrainingData.py" ]