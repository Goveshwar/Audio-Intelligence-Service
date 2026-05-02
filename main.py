
'''
#13/02
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import logging

app = FastAPI()



@app.get("/")
def read():
    return{"message": "Hello FastAPI"}


class weightage(BaseModel):
    invoice_number_wtg : float
    customer_name_wtg: float
    po_number_wtg : float
    amount_wtg : float


class priority(BaseModel):
    invoice_number_priority : int
    customer_name_priority: int
    po_number_priority: int
    amount_priority: int


class requestdata(BaseModel):
    token : str
    customer_name : str
    weightage : weightage
    priority: priority



@app.post("/user")
def createuser(user:requestdata):
    try:
        if user.customer_name != "XYZ Pvt Ltd":
            return{"message":"Enter a correct name", "status_code":4001}

        print(type(user.weightage.invoice_number_wtg))

        totalweight = (
            user.weightage.invoice_number_wtg + user.weightage.customer_name_wtg + user.weightage.po_number_wtg + user.weightage.amount_wtg
        )
        print(totalweight, type(totalweight))
        type(totalweight)
        if totalweight != 1.0:
            return{"message": "The total value should be equal to 1.0", "status_code":4002}

        priorityvalue = {
            user.priority.invoice_number_priority,
            user.priority.customer_name_priority,
            user.priority.po_number_priority,
            user.priority.amount_priority
        }
        count=0
        for i in priorityvalue:
            if i not in range(1,5):
                return{"message":"Values must be in the range of 1 to 4", "status_code":4003}

        if len(set(priorityvalue)) != len(priorityvalue):
            return{"message":"Values should be unique", "status_code":4004}

        return {"message":"The customername,totalweight and priorityvalues are unique and everything is correct", "status": "success", "status_code":200}
    except Exception:
        return{"message":"Unusual day try again", "status_code":4004}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5000, reload=True)
'''


#14/02
'''
import uvicorn
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from pydantic import BaseModel, ValidationError
import logging
import json
import asyncio
import websockets

app = FastAPI()


@app.get("/")
def read():
    return{"message": "Hello FastAPI"}


class fleightage(BaseModel):
    invoice_number_wtg :oat
    customer_name_wtg: float
    po_number_wtg : flo
    +at
    amount_wtg : float


class priority(BaseModel):
    invoice_number_priority : int
    customer_name_priority: int
    po_number_priority: int
    amount_priority: int


class requestdata(BaseModel):
    token : str
    customer_name : str
    weightage : weightage
    priority: priority


@app.post("/user")
def createuser(user:requestdata):
    try:
        if user.customer_name != "XYZ Pvt Ltd":
            return{"message":"Enter a correct name", "status_code":4001}

        #print(type(user.weightage.invoice_number_wtg))

        totalweight = (
            user.weightage.invoice_number_wtg + user.weightage.customer_name_wtg + user.weightage.po_number_wtg + user.weightage.amount_wtg
        )
        #print(totalweight, type(totalweight))
        #type(totalweight)

        if totalweight != 1.0:
            return{"message": "The total value should be equal to 1.0", "status_code":4002}

        priorityvalue = {
            user.priority.invoice_number_priority,
            user.priority.customer_name_priority,
            user.priority.po_number_priority,
            user.priority.amount_priority
        }
        count=0
        for i in priorityvalue:
            if i not in range(1,5):
                return{"message":"Values must be in the range of 1 to 4", "status_code":4003}

        if len(set(priorityvalue)) != len(priorityvalue):
            return{"message":"Values should be unique", "status_code":4004}

        return {"message":"The customername,totalweight and priorityvalues are unique and everything is correct", "status": "success", "status_code":200}
    except Exception:
        return{"message":"Unusual day try again", "status_code":4004}

@app.websocket("/creatuser")
async def websocket_createuser(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            raw_data = await websocket.receive_json()
            # data = requestdata(**raw_data)
            raw_data
            #print(raw_data)
            logging.info("websocket connected")
            if raw_data.get("action") == "start":
                msg = "Yes we received your request process"
                await websocket.send_text(msg)
            else:
                msg = "Connected bt data is not correct"
                await websocket.send_text(msg)
    


    except Exception as e:
        print("Client disconnected there might some issue while connecting")

if __name__ == "__main__":
    uvicorn.run("main:app", port=5000, reload=True)

    '''

#16/02
'''

import uvicorn
from fastapi import FastAPI, UploadFile, File, Form
import whisper
import shutil
import os
import uuid
from gtts import gTTS
from fastapi.responses import FileResponse
app = FastAPI()

model = whisper.load_model("tiny")

@app.post("/transcribe")
async def transcribe_audio(file:UploadFile = File(...)):
    try:
        extension = file.filename.split(".")[-1]
        tempfilename = f"{uuid.uuid4()}{extension}"
        with open(tempfilename, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

            result = model.transcribe(tempfilename, language = "en", fp16= False)
            text = result["text"]
            

            os.remove(tempfilename)


            return{
                "filename":file.filename,
                "trascription": result["text"]
            }
    except Exception as e:
        return {"message": str(e)}
    
if __name__ == "__main__":
    uvicorn.run("main:app", port=5000, reload=True)
'''
'''
import uvicorn
from fastapi import FastAPI, UploadFile, File, Form
import whisper
import shutil
import os
import uuid
from gtts import gTTS
from fastapi.responses import FileResponse
app = FastAPI()

model = whisper.load_model("tiny")

def remove_file(path: str):
    if os.path.exists:   
        os.remove(path)

@app.post("/speechtotext")
async def speechtotext(text: str = Form(...), lang: str = Form("en")):
    try:
        filename = f"{uuid.uuid4()}.mp3"
        tts=gTTS(text,lang=lang)
        tts.save(filename)


        return FileResponse(filename, media_type="audio/mpeg", filename="speech.mp3")
    except Exception as e:
        return {"message": str(e)}

    
if __name__ == "__main__":
    uvicorn.run("main:app", port=5000, reload=True)


'''
'''
from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import uvicorn

app = FastAPI()
client = OpenAI(api_key = "")

class Request(BaseModel):
    message: str

@app.post("/ask")
async def ask(req:Request):
    response = client.chat.completions.create(
        model = "gpt-40-mini",
        message = [{
            "role":"system", "content": " you helpful assistant"
        },
        {
            "role": "user", "content":req.message
        }]
    )
    return{"reply":response.choice[0].message.content}

if __name__ == "__main__":
    uvicorn.run("main:app", port=5000, reload=True)

'''
'''
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline

app = FastAPI()
qa = pipeline("question-answering")

class Qarequest(BaseModel):
    context: str
    question: str

@app.post("/ask")
async def ask(req: Qarequest):
    result = qa({
        "context": req.context, "question": req.question
    })
    return{"answer":result["answer"]}


if __name__ == "__main__":
    uvicorn.run("main:app", port=5000, reload=True)

'''
#17/02
'''
import torch 
import uvicorn
import uuid
import shutil
import librosa
from gtts import gTTS
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from gtts import gTTS
from transformers import WhisperProcessor, WhisperForConditionalGeneration
from transformers import pipeline
from pydantic import BaseModel
import soundfile as sf
import os
from fastapi.responses import FileResponse

app = FastAPI()

processor = WhisperProcessor.from_pretrained("openai/whisper-large")
model =  WhisperForConditionalGeneration.from_pretrained("openai/whisper-large")

text_transformer = pipeline("text-generation", model="gpt2")


def remove_file(path: str):
    if os.path.exists(path):   
        os.remove(path)

@app.post("/transcribe")
async def transcribe_audio(file:UploadFile = File(...)):
    try:
        extension = file.filename.split(".")[-1]
        tempfilename = f"{uuid.uuid4()}.{extension}"
        with open(tempfilename, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        audio, rate = librosa.load(tempfilename, sr=16000)
        input_features = processor(audio, return_tensors ="pt").input_features
        logits = model.generate(input_features)
        transcription = processor.decode(logits[0], skip_special_tokens= True)

        remove_file(tempfilename)

        return{
            "filename":file.filename,
            "transcription": transcription
        }
    except Exception as e:
        return {"message": str(e)}

@app.post("/speechtotext")
async def speechtotext(text: str = Form(...), lang: str = Form("en")):
    try:

        transformer_output = text_transformer(text, max_length=150, num_return_sequences=1)


        generated_text = transformer_output[0]['generated_text']

        print("Generated Text:", generated_text)  


        filename = f"{uuid.uuid4()}.mp3"
        tts = gTTS(generated_text, lang=lang)
        tts.save(filename)

        return FileResponse(filename, media_type="audio/mpeg", filename="speech.mp3")
    except Exception as e:
        return {"message": str(e)}

    
if __name__ == "__main__":
    uvicorn.run("main:app", port=5000, reload=True)
'''

'''
from transformers import pipeline, GPT2Tokenizer, GPT2LMHeadModel

tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2")
tokenizer.pad_token = tokenizer.eos_token

generator = pipeline("text-generation", model=model, tokenizer=tokenizer)

input_text = input("Enter your input: ")


generated_text = generator(
    input_text, 
    max_length=50, 
    num_return_sequences=1,
    truncation=True,  
    padding=True      
)

print("Generated text: ", generated_text[0]['generated_text'])

'''

#18/02

import uvicorn
from fastapi import FastAPI, UploadFile, File, HTTPException
import whisper
import shutil
import os
import uuid
from transformers import pipeline, T5ForConditionalGeneration, T5Tokenizer
import torch
from gtts import gTTS
import requests
from fastapi.responses import FileResponse

app = FastAPI()
# openapi_key = "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"

# def get_gpt3_response(prompt):
#     try:
#         response = openai.chat_Completion.create(
#             model="gpt-3.5-turbo",  # Use the engine you want (davinci, curie, etc.)
#             prompt=prompt,
#             max_tokens=150,  # Adjust the token limit based on your needs
#             temperature=0.7,
#             top_p=1.0,
#             top_k=40,
#             frequency_penalty=0.0,
#             presence_penalty=0.0
#         )
#         return response.choices[0].text.strip()
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

stt_model = whisper.load_model("tiny")
generator = pipeline("text-generation", model="gpt2")

# model_id = T5ForConditionalGeneration.from_pretrained("t5-small")
# tokenizer = T5Tokenizer.from_pretrained("t5-small")


# LLM= "http://192.168.0.243:9090/v1/chat/completions"

# response = requests.get(LLM)

# if response.status_code == 200:
#     print("Request successfull")
#     print("Response data: ", response.json())
# else:
#     print("Response failed")

def remove_file(path: str):
    if os.path.exists(path):
        os.remove(path)

@app.post("/process_audio")
async def process_audio(file: UploadFile = File(...)):
    try:

        extension = file.filename.split(".")[-1]
        tempfilename = f"{uuid.uuid4()}.{extension}"
        with open(tempfilename, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    

        result = stt_model.transcribe(tempfilename, language="en", fp16=False)
        transcribed_text = result["text"]  
        print(transcribed_text)


        os.remove(tempfilename)
        #prompt = "you are voice bot who will help users to solve queries"
        #input_text = f"{prompt} {transcribed_text}"
        input_text = transcribed_text

        # inputs = tokenizer(input_text, return_tensors="pt", truncation=True, padding = True)

        # outputs = model_id.generate(**inputs)
        

        # gpt_answer = tokenizer.decode(outputs[0], skip_special_tokens = True, lang = "en")
        # print(f"Genrated answer: {gpt_answer}")

        #question = input_text
        gpt_result = generator(input_text, max_length=100, num_return_sequences=1, temperature=0.7, top_p=0.9, top_k=50, no_repeat_ngram_size=2)
        gpt_answer = gpt_result[0]['generated_text'].strip()
        #gpt_answer = get_gpt3_response(input_text)
        print(gpt_answer)

        tts_filename = f"{uuid.uuid4()}.mp3"
        tts = gTTS(gpt_answer, lang='en')
        tts.save(tts_filename)



        return FileResponse(tts_filename, media_type="audio/mpeg", filename="output_speech.mp3")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)

'''

import requests

LLM= "http://192.168.0.243:9090/v1/chat/completions"

response = requests.post(LLM)

if response.status_code == 200:
    print("Request successfull")
    print("Response data: ", response.json())
else:
    print("Response failed")

# if __name__ == "__main__":
#     uvicorn.run("main:app", port=8000, reload=True)

'''
'''

#19/02

import uvicorn
from fastapi import FastAPI, UploadFile, File, HTTPException, WebSocket, WebSocketDisconnect
import whisper
import shutil
import logging
import logging
import os
import uuid
from transformers import pipeline, T5ForConditionalGeneration, T5Tokenizer
import torch
from gtts import gTTS
import requests
import base64
from fastapi.responses import FileResponse
import asyncio

app = FastAPI()


stt_model = whisper.load_model("tiny")
generator = pipeline("text-generation", model="gpt2")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



def remove_file(path: str):
    if os.path.exists(path):
        os.remove(path)

@app.post("/process_audio")
async def process_audio(file: UploadFile = File(...)):
    try:
        
        extension = file.filename.split(".")[-1]
        tempfilename = f"{uuid.uuid4()}.{extension}"
        with open(tempfilename, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        result = stt_model.transcribe(tempfilename, language="en", fp16=False)
        transcribed_text = result["text"]  
        print(transcribed_text)
        os.remove(tempfilename)
        #prompt = "you are voice bot who will help users to solve queries"
        #input_text = f"{prompt} {transcribed_text}"
        input_text = transcribed_text
        # inputs = tokenizer(input_text, return_tensors="pt", truncation=True, padding = True)
        # outputs = model_id.generate(**inputs)
        # gpt_answer = tokenizer.decode(outputs[0], skip_special_tokens = True, lang = "en")
        # print(f"Genrated answer: {gpt_answer}")
        #question = input_text
        gpt_result = generator(input_text, max_length=100, num_return_sequences=1, temperature=0.7, top_p=0.9, top_k=50, no_repeat_ngram_size=2)
        gpt_answer = gpt_result[0]['generated_text'].strip()
        #gpt_answer = get_gpt3_response(input_text)
        print(gpt_answer)
        tts_filename = f"{uuid.uuid4()}.mp3"
        tts = gTTS(gpt_answer, lang='en')
        tts.save(tts_filename)
        return FileResponse(tts_filename, media_type="audio/mpeg", filename="output_speech.mp3")
        await websocket.tts_filename
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.websocket("/process_audio_ws")
async def process_audio_ws(websocket: WebSocket):
    await websocket.accept()
    try:
        logger.info("WebSocket connected.")
        
        while True:
            try:

                message = await websocket.receive_text()
                audio_file = base64.b64decode(message)
                logger.info(f"Received audio data of size {len(audio_file)} bytes.")


                tempfilename = f"{uuid.uuid4()}.mp3"
                with open(tempfilename, "wb") as temp_file:
                    temp_file.write(audio_file)


                logger.info("Transcribing audio...")
                try:
                    result = stt_model.transcribe(tempfilename, language="en", fp16=False)
                    transcribed_text = result["text"]
                    logger.info(f"Transcribed text: {transcribed_text}")
                except Exception as e:
                    logger.error(f"Error during transcription: {e}")
                    await websocket.send_text("Error during transcription.")
                    continue


                logger.info("Generating GPT response...")
                try:
                    gpt_result = generator(
                        transcribed_text, 
                        max_length=100, 
                        num_return_sequences=1, 
                        temperature=1.8, 
                        top_p=0.9, 
                        top_k=50, 
                        no_repeat_ngram_size=2,
                        truncation=True
                    )
                    gpt_answer = gpt_result[0]['generated_text'].strip()
                    logger.info(f"Generated GPT answer: {gpt_answer}")
                except Exception as e:
                    logger.error(f"Error during GPT generation: {e}")
                    await websocket.send_text("Error during GPT generation.")
                    continue


                logger.info("Converting GPT response to speech...")
                tts_filename =pipeline f"{uuid.uuid4()}.mp3"
                try:
                    tts = gTTS(gpt_answer, lang='en')
                    tts.save(tts_filename)
                    logger.info("TTS conversion successful.")
                except Exception as e:
                    logger.error(f"Error during TTS conversion: {e}")
                    await websocket.send_text("Error during text-to-speech conversion.")
                    continue


                logger.info(f"Sending audio back in Base64-encoded chunks...")
                with open(tts_filename, "rb") as audio_file:
                    audio_data = audio_file.read()
                    base64_audio = base64.b64encode(audio_data).decode('utf-8')
                    # while chunk := audio_file.read(4096):  
                    #     base64_chunk = base64.b64encode(chunk).decode('utf-8')  
                    #     await websocket.send_text(base64_chunk)
                    #     logger.debug(f"Sent chunk of size: {len(chunk)} bytes")

                await websocket.send_text(base64_audio)
                logger.debug(f"Sent entire audio data of size: {len(base64_audio)} characters.")


                remove_file(tempfilename)
                remove_file(tts_filename)

            except Exception as e:
                logger.error(f"Unexpected error during audio processing: {e}")
                await websocket.send_text(f"Error processing the audio file: {str(e)}")
                break

    except WebSocketDisconnect:
        logger.info("Client disconnected.")
    
    except Exception as e:
        logger.error(f"Unexpected error in WebSocket communication: {e}")
        await websocket.close()


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)

'''
