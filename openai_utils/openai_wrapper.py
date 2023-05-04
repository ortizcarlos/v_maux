import openai 
from time import sleep

COMPLETIONS_MODEL = "text-davinci-003"
embed_model = "text-embedding-ada-002"

def chat_completation(prompt):
    response = openai.ChatCompletion.create(
              model="gpt-3.5-turbo",
              messages=[
                #{"role": "system", "content": "Tu eres un asistente para responder preguntas sobre programa de gobierno de un candidato politico."},
                {"role": "user", "content": prompt}
            ]
    )

    result = ''
    for choice in response.choices:
       result += choice.message.content

    return result


def invoke_gpt(prompt):

    prediction = openai.Completion.create(
                    prompt=prompt,
                    temperature=0.5,
                    max_tokens=120,
                    top_p=1,
                    frequency_penalty=0,
                    presence_penalty=0,
                    model=COMPLETIONS_MODEL)["choices"][0]["text"].strip(" \n")
    return prediction
    
'''
Calls openai's embeddings endpoint passing a list of sentences

sentences : ['sentence 1','sentence 2', ... sn]

return a list of embeddings
[embeddings 1, embeddings 2 , ..., embeddings n]
'''
def get_embeddings(sentences) -> list:

    try:
        response = openai.Embedding.create(input=sentences, engine=embed_model)
    except:
        done = False
        while not done:
            sleep(5)
            try:
                response = openai.Embedding.create(input=sentences, engine=embed_model)
                done = True
            except:
                pass
            
    embeds = [record['embedding'] for record in response['data']]
    return embeds

