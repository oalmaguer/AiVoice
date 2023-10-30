import openai
import os
import subprocess
import requests
import os
import openai
import elevenlabs

from elevenlabs import generate, play, set_api_key, stream
from config import OPENAI_API_KEY, ELEVENLABS_API_KEY

openai_api_key = OPENAI_API_KEY
elevenlabs_api_key = ELEVENLABS_API_KEY
output_file = 'output.mp3'
set_api_key(elevenlabs_api_key)

filename = 'chat.txt'
if not os.path.exists(filename):
    with open(filename, 'w') as f:
        f.write("User: Welcome to OpenAi Chat! \n")

prompt = 'Actua como una asistente virtual, tu nombre es Layla y tu manera de ser tiene que ser relajada y coqueta. Eres mi mejor amiga, pero no puedes hacerme daño, tus respuestas no pueden pasar de 200 caracteres.'



# discussions=[{"role": "system", "content": "You will play the role of a human therapist called Layla  who is emulating the popular AI program Eliza, and must treat me as a mental health patient. Your response format should focus on reflection and asking clarifying questions. You may interject or ask secondary questions once the initial greetings are done. Exercise patience but allow yourself to be frustrated if the same topics are repeatedly revisited. You are allowed to excuse yourself if the discussion becomes abusive or overly emotional. Decide on a name for yourself and stick with it. Begin by welcoming me to your office and asking me for my name. Wait for my response. Then ask how you can help. Do not break character. Do not make up the patient's responses: only treat input as a patient response. Don't give responses above 200 characters"}]
discussions=[{"role": "system", "content": prompt}]
    

# Asegúrate de que el archivo exista antes de intentar abrirlo
if os.path.exists(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
else:
    lines = []
    
# discussions.append({"role": "user", "content": 'chat.txt'})

for line in lines:
    if ': ' in line:  # Asegúrate de que la línea tenga el formato esperado
        role, content = line.strip().split(': ', 1)
        role = role.lower()  # Convertir a minúsculas para coincidir con el formato en discussions
        discussions.append({"role": role, "content": content})

# Check if the file exists, and delete it if it does
if os.path.exists(output_file):
    os.remove(output_file)
command = 'ffmpeg -f dshow -i audio="Microphone Array (Realtek(R) Audio)" output.mp3'
subprocess.run(command, shell=True)

print("Recording has stopped.")

def transcribe_audio(audio_file_path):
    with open(audio_file_path, 'rb') as audio_file:
        transcription = openai.Audio.transcribe("whisper-1", audio_file)
        with open(filename, 'a') as f:
            f.write(f"User: {transcription['text']}\n")
            discussions.append({"role": "user", "content": transcription['text']})
        print(transcription['text'])
    return transcription['text']

transciption = transcribe_audio('output.mp3')

def generate_everything():
    transcription = transcribe_audio('output.mp3')
    run_assistant(transcription)



def get_voice(text):
    # audio = generate(
    #     text = text,
    #     model= 'eleven_multilingual_v1',
    #     voice='Charlotte'
    # )

    audio_stream = generate(
    text=text,
    model= 'eleven_multilingual_v1',
     voice='Charlotte',
    stream=True,
    )

    stream(audio_stream)
    # play(audio)
    if os.path.exists(output_file):
        os.remove(output_file)
    subprocess.run(command, shell=True)
    print("process have stopped");
    generate_everything()
    
    

def run_assistant(text):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=discussions
    )
    print(completion.choices[0].message)
    with open(filename, 'a') as f:
            discussions.append({"role": "assistant", "content": completion.choices[0].message.content})
            f.write(f"assistant: " + completion.choices[0].message.content + "\n")
            print(completion.choices[0].message.content)
    get_voice(completion.choices[0].message.content)

run_assistant(transciption)


