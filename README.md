# Backend installation

### Create virtual env & install dependencies

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Setup DB
#### Set up db configuration in .env
```
cp .env.example .env
```
#### Setup db in mysql according to .env

### Run 

```
source venv/bin/activate
python eflask.py
```

### Optional
#### Add words data from file to db
```
python -m build_db.add_words_to_db
```

#### Update db schema
+ Delete folder `migrations`.
+ Delete table `alembic_version` in db.
+ Exec shell script: `./update_db_schema`
#### In order to exec video API
Update pytube to convert youtube caption from xml to srt
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

### Get user avatar url 
`localhost:5001/static/avatars/<avatar_url>`
(`avatar_url` is a field returned from login api)
