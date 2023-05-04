
from twilio.twiml.messaging_response import MessagingResponse
from typing import Optional

import uvicorn
from fastapi import FastAPI, File, UploadFile, Form,Response
from fastapi.middleware.cors import CORSMiddleware

from audio.audio_processor import AudioProcessor
import config.SystemConfig as cfg

import config.AppObjects as appObjects
from config.envloader import load_env
from prompt_utils.prompt_builder import PoliticAssistantPromptBuilder

from audio.voice_decoder import VoiceDecoder
from audio.media_helper import fetch_resource_from_twilio
from PlatformExceptions import AppException,InvalidInputException

import logging
import threading
import queue

main_queue = queue.Queue()
audio_processor = AudioProcessor(main_queue)
prompt_builder = PoliticAssistantPromptBuilder()
threading.Thread(target=audio_processor.start, daemon=True).start()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def database_connect():
    load_env()
    appObjects.init_coordinator(cfg.vector_index_name)
    print("Coordinator started")

@app.post("/bot-status")
async def bot_status():
    response = MessagingResponse() 
    response.message("status")
    return Response(content=str(response), media_type="application/xml")

@app.post('/bot-receiver')
async def bot_receiver(To: str = Form(...), 
                       From: str = Form(...),
                       Body: Optional[str] = Form('...'),
                       MediaUrl0: Optional[str] = Form('')):
    
    response = MessagingResponse() 
    query = Body.strip()

    if (len(MediaUrl0)>0):
       datadict = {'voice_file':MediaUrl0,
                   'destination':From,
                   'origin': To}
       audio_processor.schedule_audiofile(datadict)
       response.message('Tu nota de voz fue recibida, en un momento recibiras una respuesta') 
       return Response(content=str(response), media_type="application/xml")   

    if not (query[-1]=='?' or len(query)==0 ): 
      response.message('Lo siento, tu mensaje no parece ser una pregunta') 
      return Response(content=str(response), media_type="application/xml")   

    llm_response = appObjects.coordinator.answer(prompt_builder,query)
    response.message(llm_response)
   
    return Response(content=str(response), media_type="application/xml")

# Run the FastAPI app
if __name__ == "__main__":
  uvicorn.run(app, host="0.0.0.0", port=8000)