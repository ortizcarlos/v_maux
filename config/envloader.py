import config.SystemConfig as cfg
import openai
from jproperties import Properties


def load_env():
  configs = Properties()
  with open('properties.txt', 'rb') as config_file:
    configs.load(config_file)

  cfg.pinecone_api_key = configs.get("pinecone_api_key").data
  cfg.pinecone_env = configs.get("pinecone_env").data
  cfg.vector_index_name = configs.get("vector_index_name").data
  cfg.open_ai_key = configs.get("open_ai_key").data
  cfg.addenv_var("twilio.account_sid",configs.get("twilio.account_sid").data)
  cfg.addenv_var("twilio.auth_token",configs.get("twilio.auth_token").data)
  
  openai.api_key = cfg.open_ai_key
