## Run this command in terminal  before executing this program
## rasa run -m models --endpoints endpoints.yml --port 5005 --credentials credentials.yml
## and also run this in seperate terminal
## rasa run actions

import requests
import speech_recognition as sr     # import the library
import subprocess
from gtts import gTTS
from google_trans_new import google_translator  
from playsound import  playsound
import random
import os

# sender = input("What is your name?\n")

bot_message = ""
message=""
translator = google_translator()
# translator = Translator(to_lang='hi')
translation = translator.translate("hello", "hi")

r = requests.post('http://localhost:5005/webhooks/rest/webhook', json={"message": "Hello"})

print("Bot says, ",end=' ')
for i in r.json():
    bot_message = i['text']
    print(f"{bot_message}")

myobj = gTTS(text=translator.translate("Hi", 'hi'),lang='hi')
myobj.save("welcome.mp3")
print('saved')
# Playing the converted file
# subprocess.call(['cvlc', "welcome.mp3", '--play-and-exit'])
playsound("welcome.mp3")

while bot_message != "Bye" or bot_message!='thanks':
    
    r = sr.Recognizer()  # initialize recognizer
    with sr.Microphone() as source:  # mention source it will be either Microphone or audio files.
        print("Speak Anything :")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)  # listen to the source
        print("hi")
        try:
            message = r.recognize_google(audio)  # use recognizer to convert our audio into text part.
            # translator = Translator(to_lang='en')
            print("You said : {}".format(translator.translate(message, "en")))

        except:
            print("Sorry could not recognize your voice")  # In case of voice not recognized  clearly
    if len(message)==0:
        continue
    print("Sending message now...")

    r = requests.post('http://localhost:5005/webhooks/rest/webhook', json={"message": translator.translate(message, "en")})

    print("Bot says, ",end=' ')
    for i in r.json():
        if('text' in i):
            bot_message = i['text']
        if('image' in i):
            bot_message = i['image']
        print(f"{bot_message}")
    # translator = Translator(to_lang='hi')
    myobj = gTTS(text=translator.translate(bot_message, "hi"))
    name = random.randint(100, 999)
    myobj.save(str(name) +".mp3")
    print('saved')
    # Playing the converted file
    # subprocess.call(['cvlc', "welcome.mp3", '--play-and-exit'])
    playsound(str(name)+".mp3")
    os.remove(str(name)+".mp3")