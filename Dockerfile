FROM ubuntu
RUN apt-get -y update && apt-get -y upgrade && apt-get -y install python3-pip net-tools vim && pip install awscli requests numpy pandas matplotlib boto3
RUN mkdir -p root/lambda-code root/python root/json
COPY lambda-code root/lambda-code/
COPY python root/python/
COPY json root/json/
WORKDIR /root
