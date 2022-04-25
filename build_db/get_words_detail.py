import requests
import json

def search(word):
    url = f'https://api.dictionaryapi.dev/api/v2/entries/en/{word}'
    response = requests.request("GET", url, headers={}, data={})
    if response.status_code == 200:
        return parse(json.loads(response.text)[0])
    else:
        return {'word': word, 'error': 'Not found'}
    
def parse(data):
    result = {}
    result['word'] = data['word']
    result['ipa'] = parse_ipa(data)
    result['audio_url'] = parse_audio_url(data)
    result['definitions'] = parse_definitions(data)

    return result

def parse_ipa(data):
    ipa = ''
    for phonetic in data['phonetics']:
        if 'text' in phonetic:
            ipa = phonetic['text']
    return ipa

def parse_audio_url(data):
    audio_url = ''
    for phonetic in data['phonetics']:
        if 'audio' in phonetic:
            audio_url = phonetic['audio']
    return audio_url

def parse_definitions(data):
    definitions = []
    for meaning in data['meanings']:
        for i in range(len(meaning['definitions'])):
            definition = meaning['definitions'][i]
            definition['lexical_category'] = meaning['partOfSpeech']
            definition['meaning'] = definition['definition']
            del definition['synonyms']
            del definition['antonyms']
            del definition['definition']

            definitions.append(definition)
    return definitions


INP_FILE = 'words.txt'
OUT_FILE = 'words_detail.txt'

if __name__ == '__main__':
    with open(INP_FILE, 'r') as inp:
        with open(OUT_FILE, 'a') as out:
            lines = inp.readlines()
            current_line = 47185
            last_line = len(lines)

            for i in range(current_line, last_line):
                word = lines[i].strip()
                out.write(f'{json.dumps(search(word))}\n')