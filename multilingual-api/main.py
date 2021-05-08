from fastapi import FastAPI
from pydantic import BaseModel
import requests
from google_trans_new import google_translator  

app = FastAPI()
translator = google_translator()

class Obj(BaseModel):
    msg: str
    lang: str

@app.get("/")
async def root():
    return {"message": "Welcome to ABInBev Multilingual API"}

@app.post("/abinbev")
async def abinbev(obj: Obj):
    print(f'orignal -> {obj.msg}')
    obj.msg = translator.translate(obj.msg, 'en')
    print(f'converted into eng -> {obj.msg}')

    r = requests.post('http://localhost:5005/webhooks/rest/webhook', json={"message": obj.msg})

    res = []
    for i in r.json():
        bot_message = i['text']
        bot_message_lang = translator.translate(bot_message, obj.lang)
        res.append(bot_message_lang)
    return res
