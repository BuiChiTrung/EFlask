FROM ubuntu:20.04 AS db-prepare
ENV DEBIAN_FRONTEND=noninteractive
RUN apt update && apt install -y mysql-server python3-pip libmysqlclient-dev

WORKDIR /eflask
COPY . .
RUN pip3 install -r requirements.txt

ENV HOSTNAME=localhost
ENV PORT=3306
ENV DB_USER=root
ENV DATABASE=EFlask
ENV SECRET_KEY="very secret key"

RUN mysqld & \
    mysqladmin ping 2> /dev/null; \
    while [ $? -eq 1 ]; do mysqladmin ping 2> /dev/null; done; \
    echo "CREATE DATABASE $DATABASE;" | mysql; \
    echo "from app import create_app,db; db.create_all(app=create_app())" | python3 -; \
    python3 -m build_db.add_words_to_db; \
    mysqldump --databases $DATABASE > data.sql

FROM mysql:8
COPY --from=db-prepare /eflask/data.sql /docker-entrypoint-initdb.d

