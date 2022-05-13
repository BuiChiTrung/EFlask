FROM python:3.8-alpine
RUN apk add mariadb-connector-c-dev gcc musl-dev libffi-dev
WORKDIR /EFlask/Backend
COPY . .
RUN pip install -r requirements.txt
EXPOSE 5001
ENTRYPOINT [ "python", "eflask.py" ]
