FROM ubuntu
RUN apt-get -y update && apt-get -y upgrade && apt-get -y install python3-pip net-tools vim && pip install awscli requests numpy pandas matplotlib
RUN mkdir -p root/scripts root/python
COPY scripts root/scripts/
COPY python root/python/
WORKDIR /root
