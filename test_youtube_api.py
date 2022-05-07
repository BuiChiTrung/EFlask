# Import Pytube module to use API
from unittest.mock import NonCallableMagicMock
from pytube import YouTube


video_url = 'https://www.youtube.com/watch?v=hNGoDCTLS-E&ab_channel=Kallmekris'
yt = YouTube(video_url)

caption = None

print(yt.captions)
if 'en' in yt.captions:    
    caption = yt.captions.get_by_language_code('en')
elif 'a.en' in yt.captions:
    caption = yt.captions.get_by_language_code('a.en')

res = caption.generate_srt_captions()
print(res)