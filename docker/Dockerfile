FROM python:3

EXPOSE 5001

WORKDIR /eflask/Backend/

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY xml_to_srt.py .
RUN sed 's/xml_caption_to_srt/xml_caption_to_srt_old/' /usr/local/lib/python3.10/site-packages/pytube/captions.py
RUN cat xml_to_srt.py >> /usr/local/lib/python3.10/site-packages/pytube/captions.py

COPY .. .

CMD ["python", "eflask.py" ]