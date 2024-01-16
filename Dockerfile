FROM python:3.10

LABEL maintainer="Zeki Ahmet Bayar <zeki@liman.dev>"

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN apt update && apt install unzip poppler-utils libreoffice -y

RUN mkdir reports results

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./ /code/

CMD ["python3", "main.py"]