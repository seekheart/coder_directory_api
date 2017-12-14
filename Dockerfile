FROM python:3.6
MAINTAINER mike tung<miketung2013@gmail.com>

COPY ./app.py /app/app.py
COPY ./coder_directory_api /app/coder_directory_api
COPY ./entrypoint.sh /app/entrypoint.sh
COPY ./requirements.txt /app/requirements.txt

WORKDIR app

RUN pip install -r requirements.txt
RUN rm requirements.txt


ENTRYPOINT ["./entrypoint.sh"]