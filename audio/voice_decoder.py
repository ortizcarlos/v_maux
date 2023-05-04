#from whisper_jax import FlaxWhisperPipline
import whisper
import os
# JIT compile the forward call - slow, but we only do once

class VoiceDecoder():
    
    def __init__(self):
        # instantiate pipeline
        #self.pipeline = FlaxWhisperPipline("openai/whisper-small")
        self.model = whisper.load_model("small")

    def to_text(self,voice_file:str):
        print(f'generating transcript from file {voice_file}')
        prediction = self.model.transcribe(voice_file)
        return prediction["text"]
        '''
        prediction = self.pipeline(voice_file)
        return prediction['text']
        '''

if __name__=='__main__':
   vd = VoiceDecoder()
   text = vd.to_text('e93c03af-eaa5-11ed-93cb-94e23c9932f1.ogg')
   print(text)



