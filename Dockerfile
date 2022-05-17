FROM python:3.10-alpine

WORKDIR /usr/src

ADD requirements.txt .
RUN pip install --no-cache-dir -r ./requirements.txt

ADD . .

RUN mkdir data

CMD ["python", "./run.py"]
