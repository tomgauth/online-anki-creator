import genanki
import random

def gen_anki_id():
    return random.randrange(1 << 30, 1 << 31)

my_model = genanki.Model(
  gen_anki_id(),
  'Simple Model',
  fields=[
    {'name': 'Question'},
    {'name': 'Answer'},
    {'name': 'Audio_one'},
    {'name': 'Audio_two'}
  ],
  templates=[
    {
      'name': 'Card 1',
      'qfmt': '{{Question}} </br> {{Audio_one}}',
      'afmt': '''{{FrontSide}}
      <hr id=answer>
        {{Audio_two}}
        <div style="font-family: Futura; font-size: 20px;">{{Answer}}</div>        
        <div style= "color:#00afe4; font-family: Futura; font-size: 10px;">©Online Anki Generator</div>''',
    },
  ])