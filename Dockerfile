FROM python:3.6.3
MAINTAINER Mike Tung <miketung2013@gmail.com>

COPY coder_directory_api /coder_directory_api
COPY requirements.txt /requirements.txt
COPY entrypoint.sh /entrypoint.sh
RUN pip install -r requirements.txt

EXPOSE 3000

ENTRYPOINT ["/entrypoint.sh"]
