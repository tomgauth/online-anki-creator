# This Python file uses the following encoding: utf-8

# Add subtitles to a csv file easily
# find lines matching the word you're looking for
# preview the lines?
# Create anki flashcards from the selected lines

# Select the another language to add to the csv (for translation)
# Create anki flashcards from all the lines of a video


from airtable import Airtable
import pandas as pd
import genanki
import random
from datetime import datetime
import time
import moviepy
from gtts import gTTS
from pathlib import Path

from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip



# split video
def srt_time_to_sec(time_srt):
  td = datetime.strptime(time_srt,'%H:%M:%S,%f') - datetime(1900,1,1)
  return td.total_seconds()


api_key = input("Paste your API Key here:  ")
video_name = Path(input("copy paste the name of the video to use (should be in the same folder as this script):  "))
video_id = input("The video ID:  ")

# 6_weeks_Challenge_Patrick.mp4
# keyKRBU0MXfsukETM

key_sentences = Airtable('app3qY4PvmhbRYcfj', 'Key Sentences', api_key = api_key)


video_recognition = genanki.Model(
  1851172070,
  'Video Recognition',
  css="""
  .card {
 font-family: futura;
 font-size: 20px;
 text-align: center;
 color: #373f51;
 background-color: #eeebd0;
}

.media {
 margin: 2px;
}
  """,
  fields=[
    {'name': 'Video ID'},
    {'name': 'Line ID'},
    {'name': 'Video Media'},
    {'name': 'French'},
    {'name': 'English'},
    {'name': 'Sunpleman Fransé'},
    {'name': 'Phonetic IPA'},
  ],
  templates=[
    {
      'name': 'Card 1',
      'css': '',
      'qfmt': '<div class="media">{{Video Media}}</div>',
      'afmt': '{{FrontSide}}<hr id=answer><div style="font-family: Futura; font-size: 20px;">{{English}}</div><div style= font-family: Futura; font-size: 15px;>{{French}}</div><br/><div style= "color:#ee6c4d; font-family: Arial; font-size: 30px;">{{Sunpleman Fransé}}</div><br/><div style="font-family: Arial; font-size: 20px;">{{Phonetic IPA}}</div><br/><div style= "color:#00afb9; font-family: Futura; font-size: 10px;">© Hack French with Tom</div>',
    },
  ])


def generate_anki_deck(selected_video,required_video_file):
  deck_id = random.randrange(1 << 30, 1 << 31)
  video_deck = genanki.Deck(deck_id, 'flashcards deck video {}'.format(selected_video))
  package = genanki.Package(video_deck)
  formula = '{Video ID}='+str(selected_video)
  sentences = key_sentences.get_all(formula=formula,sort=[('Line ID','asc')])
  for i in range(len(sentences)):
    print('Sentence',i)
    print(sentences[i]['fields']['French'])
    starttime = srt_time_to_sec(sentences[i]['fields']['Time Start'])
    endtime = srt_time_to_sec(sentences[i]['fields']['Time Stop'])
    cut_name = 'Video_{}_Line_{}.mp4'.format(sentences[i]['fields']['Video ID'][0],sentences[i]['fields']['Line ID'])
    tag_cut_name = "[sound:{}]".format(cut_name)
    # generate the video file
    ffmpeg_extract_subclip(required_video_file, starttime, endtime, targetname=cut_name) # -c:a aac
    sentence_note = genanki.Note(
    model=video_recognition,
    fields=[sentences[i]['fields']['Video ID'][0],
      sentences[i]['fields']['Line ID'],
      tag_cut_name,
      sentences[i]['fields']['French'],
      sentences[i]['fields']['English (manual)'],
      ' ',
      ' '

      ]
    )
    video_deck.add_note(sentence_note)
    package.media_files.append(cut_name)
    print('added a sentence to video_deck')
#video_deck.add_note(new_note)
  package.write_to_file('video{}_deck.apkg'.format(selected_video))

generate_anki_deck(video_id,video_name)
