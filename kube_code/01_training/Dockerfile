FROM mcr.microsoft.com/azureml/openmpi3.1.2-ubuntu18.04:20210615.v1

# pip install
COPY requirements.txt /scripts/requirements.txt
RUN pip install -r /scripts/requirements.txt

COPY TrainOnLocal.py /scripts/TrainOnLocal.py
COPY classifier.py /scripts/classifier.py
COPY config.json /scripts/config.json

# will be overwritten by kf pipeline
ENTRYPOINT [ "python", "/scripts/TrainOnLocal.py" ]