import queue 
import logging

import config.AppObjects as appObjects
import config.SystemConfig as cfg

from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client

from audio.voice_decoder import VoiceDecoder
from audio.media_helper import fetch_resource_from_twilio
from prompt_utils.prompt_builder import PoliticAssistantPromptBuilder



answer_start = 'La siguiente es la respuesta a tu pregunta: '
prompt_builder = PoliticAssistantPromptBuilder()

class AudioProcessor():
   
   def __init__(self,q:queue):
      self.queue = q
      self.voiceDecoder = VoiceDecoder()

   def schedule_audiofile(self,datadict):
     self.queue.put(datadict)
     # Your Account SID and Auth Token from console.twilio.com
     account_sid = cfg.getenv_var("twilio.account_sid")
     auth_token  = cfg.getenv_var("twilio.auth_token")
     self.client = Client(account_sid, auth_token)

   def handle_voice_note(self,resource_url):
      local_file = fetch_resource_from_twilio(resource_url)
      transcript = self.voiceDecoder.to_text(local_file)
      return transcript
   
   def send_msg(self,destination:str,origin:str,msg:str):
      message = self.client.messages.create(
         to = destination,
         from_= origin,
         body=msg)

   def format_response(self,query,answer):
      return f" {answer_start} \n {query} \n {answer}"
                
   def start(self):
      
      while True:
         params_dict  = self.queue.get()
         voice_file   = params_dict['voice_file']
         destination = params_dict['destination']
         origin = params_dict['origin']
         try:
           query = self.handle_voice_note(voice_file)
           logging.debug(query)
           if ( len(query.strip())>0 ):
              self.send_msg(destination,origin,
                            self.format_response(query,appObjects.coordinator.answer(prompt_builder,query)))
           else:
              logging.warn('Empty voice note')
              self.send_msg(destination,origin,'Nota de voz vacia')
         except Exception as e:
            logging.error(e) 