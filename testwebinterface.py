
from twilio.twiml.messaging_response import MessagingResponse
from typing import Optional

import uvicorn
from fastapi import FastAPI, File, UploadFile, Form,Response
from fastapi.middleware.cors import CORSMiddleware

import logging
import threading
import queue


'''
main_queue = queue.Queue()
audio_processor = AudioProcessor(main_queue)
threading.Thread(target=audio_processor.start, daemon=True).start()
'''

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
    response.message(Body)
   
    return Response(content=str(response), media_type="application/xml")

# Run the FastAPI app
if __name__ == "__main__":
  uvicorn.run(app, host="0.0.0.0", port=8000)