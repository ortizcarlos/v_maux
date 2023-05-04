
from openai_utils.openai_wrapper import predict
from audio.audio_processor import AudioProcessor

import config.SystemConfig as cfg

from jproperties import Properties
import config.AppObjects as appObjects

configs = Properties()
with open('properties.txt', 'rb') as config_file:
    configs.load(config_file)

cfg.pinecone_api_key = configs.get("pinecone_api_key").data
cfg.pinecone_env = configs.get("pinecone_env").data
cfg.vector_index_name = configs.get("vector_index_name").data
cfg.open_ai_key = configs.get("open_ai_key").data

appObjects.init_coordinator(cfg.vector_index_name)

import os

directory = "./context"  # replace with the path to your directory
appObjects.coordinator.delete_vindex_content()
for filename in os.listdir(directory):
    with open(os.path.join(directory, filename), "r") as f:
            file_contents = f.read()
    reference = filename
    print(reference)
    appObjects.coordinator.index_text(file_contents,reference)

