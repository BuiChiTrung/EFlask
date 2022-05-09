FROM python:3.8-alpine
WORKDIR /EFlask/Backend
COPY . .
RUN /bin/sh -c 'pip install -r requirements.txt'
EXPOSE 5001
ENTRYPOINT [ "python", "eflask.py" ]
