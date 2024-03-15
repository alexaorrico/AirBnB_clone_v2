FROM ubuntu:20.04
ENV TZ=America/Chicago
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get update --fix-missing && apt-get upgrade -y --fix-missing
RUN apt-get install -y git
RUN apt-get install -y curl
RUN apt-get install -y python3 python3-pip
RUN apt-get install -y python3-lxml
RUN pip3 install Flask
