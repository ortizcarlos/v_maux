import requests
import uuid
from pydub import AudioSegment

def fetch_resource_from_twilio(resource_url:str,pre_mp3=False):
    r = requests.get(resource_url, allow_redirects=True)
    filename = f"./tmp/{uuid.uuid1()}"
    open(filename, 'wb').write(r.content)
    if (pre_mp3):
      AudioSegment.from_file(filename).export( filename + "mp3", format="mp3")
      filename += "mp3"
    return filename