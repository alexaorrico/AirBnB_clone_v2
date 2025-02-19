FROM python:3.4
MAINTAINER glyif <122@holbertonschool.com>

RUN git clone https://github.com/glyif/AirBnB_clone_v3.git ~/AirBnB
WORKDIR /root/AirBnB
RUN pip install -r requirements.txt

ENV HBNB_MYSQL_USER=hbnb_dev
ENV HBNB_MYSQL_PWD=hbnb_dev_pwd
ENV HBNB_MYSQL_HOST=db
ENV HBNB_MYSQL_DB=hbnb_dev_db
ENV HBNB_TYPE_STORAGE=db
ENV HBNB_API_HOST=0.0.0.0
ENV HBNB_API_PORT=5000

EXPOSE 5000

CMD ["python3", "-m", "api.v1.app"]