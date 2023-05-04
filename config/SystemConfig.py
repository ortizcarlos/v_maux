PINECONE_DEF_ENV  = 'BASE'
VECTOR_DIMENSIONS = 1536

JOB_DESCRIPTION_MIN_LEN = 30
MIN_RANKING_ITEM_COUNT = 3
TOKEN_LENGTH = 4
RESUME_SUMMARY_LENGTH = TOKEN_LENGTH * 1000

pinecone_api_key = ''
pinecone_env = ''


open_ai_key = ''
vector_index_name = ''
max_resume_tokens = 1000

mediatype_mapper = {'docx' : 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
'pdf':'application/pdf'}

props = {}

def addenv_var(key:str,value:str):
    props[key] = value

def getenv_var(key:str):
    return props[key]