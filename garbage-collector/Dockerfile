FROM python:2.7

RUN  mkdir -p /usr/src/app

WORKDIR /usr/src/app
COPY ./server/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./server/* ./
EXPOSE 8080

CMD ["python", "server.py"]