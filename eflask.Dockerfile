FROM python:3.8-alpine
RUN apk add mariadb-connector-c-dev gcc musl-dev libffi-dev
WORKDIR /eflask
COPY . .
RUN pip install -r requirements.txt && \
    CAPTIONS_FILE=$(python -c "import sys; print(next(path for path in sys.path if path.find('site-packages') >= 0))")/pytube/captions.py && \
    sed -i "s/def xml_caption_to_srt(self, xml_captions: str) -> str:/def deprecated(self, xml_captions: str) -> str:/" $CAPTIONS_FILE && \
    cat xml_to_srt.py >> $CAPTIONS_FILE
EXPOSE 5001
ENTRYPOINT [ "python", "eflask.py" ]
