# Backend installation

### Create virtual env & install dependencies

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Add env var

```
export FLASK_APP=eflask.py
export FLASK_DEBUG=true
export FLASK_RUN_PORT=5001
```

### Setup DB
Create db EFlask in mysql, then:
```
flask shell
db.create_all()
```
Add data from file to db
```
python -m build_db.add_words_to_db
```

### Migrate database (when db schema changes)

```
flask db init
flask db migrate
flask db upgrade
```

### Update pytube to convert youtube caption from xml to srt
```
# venv/lib/pytube/captions.py
def xml_caption_to_srt(self, xml_captions: str) -> str:
    """Convert xml caption tracks to "SubRip Subtitle (srt)".

    :param str xml_captions:
    XML formatted caption tracks.
    """
    segments = []
    root = ElementTree.fromstring(xml_captions)
    i=0
    for child in list(root.iter("body"))[0]:
        if child.tag == 'p':
            caption = ''
            if len(list(child))==0:
                # instead of 'continue'
                caption = child.text
            for s in list(child):
                if s.tag == 's':
                    caption += ' ' + s.text
            caption = unescape(caption.replace("\n", " ").replace("  ", " "),)
            try:
                duration = float(child.attrib["d"])/1000.0
            except KeyError:
                duration = 0.0
            start = float(child.attrib["t"])/1000.0
            end = start + duration
            sequence_number = i + 1  # convert from 0-indexed to 1.
            line = "{seq}\n{start} --> {end}\n{text}\n".format(
                seq=sequence_number,
                start=self.float_to_srt_time_format(start),
                end=self.float_to_srt_time_format(end),
                text=caption,
            )
            segments.append(line)
            i += 1
    return "\n".join(segments).strip()
```
### Run 

```
flask run
```