import openai
import os
import subprocess
import requests
import os
import openai
import elevenlabs
from elevenlabs import generate, play
openai.api_key = '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'
elevenlabs_api_key = '68961c3c88855abe86af009cf34ff208'
output_file = 'output.mp3'

# Check if the file exists, and delete it if it does
if os.path.exists(output_file):
    os.remove(output_file)
command = 'ffmpeg -f dshow -i audio="Microphone Array (Realtek(R) Audio)" output.mp3'
subprocess.run(command, shell=True)

print("Recording has stopped.")

def transcribe_audio(audio_file_path):
    with open(audio_file_path, 'rb') as audio_file:
        transcription = openai.Audio.transcribe("whisper-1", audio_file)
        print(transcription['text'])
    return transcription['text']

transciption = transcribe_audio('output.mp3')

def get_voice(text):
    audio = generate(
        text = text,
        model= 'eleven_multilingual_v2',
    )
    play(audio)
    

def run_assistant(text):
    completion = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
    {"role": "system", "content": "You are a very experienced therapist, skilled in explaining complex phsycological concepts with creative flair. You are a partner someone can talk to"},
    {"role": "user", "content": text}
  ]
    )
    print(completion.choices[0].message)
    get_voice(completion.choices[0].message.content)

run_assistant(transciption)


