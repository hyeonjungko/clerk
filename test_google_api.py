import io
import os

# Imports the Google Cloud client library
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

# Instantiates a client
client = speech.SpeechClient()

# The name of the audio file to transcribe
file_name = os.path.join(
    os.path.dirname(__file__),
    'resources',
    #'gettysburg_test.wav')
    'convo_2ppl_test.wav')

# Loads the audio into memory
with io.open(file_name, 'rb') as audio_file:
    content = audio_file.read()
    audio = types.RecognitionAudio(content=content)

# set speaker diarization configuration
diarization_config = types.SpeakerDiarizationConfig(
    enable_speaker_diarization=True,
    min_speaker_count=2,
    max_speaker_count=3)

# set speech client configuration
config = types.RecognitionConfig(
    encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
    sample_rate_hertz=44100,
    audio_channel_count=2,
    language_code='en-US',
    diarization_config=diarization_config)

# Detects speech in the audio file
response = client.recognize(config, audio)
"""
print(response)
for result in response.results:
    print('Transcript: {}'.format(result.alternatives[0].transcript))
"""
tag = 1
spoken = ""
transcript = ""
result = response.results[-1]
for word_info in result.alternatives[0].words: #Changed
        if word_info.speaker_tag==tag: #Changed
            spoken=spoken+" "+word_info.word #Changed
        else: #Changed
            transcript += "speaker {}: {}".format(tag,spoken) + '\n' #Changed
            tag=word_info.speaker_tag #Changed
            spoken=""+word_info.word #Changed

transcript += "speaker {}: {}".format(tag,spoken) #Changed
print(transcript)
