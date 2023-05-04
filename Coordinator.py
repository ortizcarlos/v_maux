from openai_utils.openai_wrapper import get_embeddings,chat_completation

from VectorDataStore import VectorDataStore
import uuid
import logging
import os
from prompt_utils.prompt_builder import PromptBuilder

class Coordinator:

    def __init__(self,vector_index_name):
        self.index_name = vector_index_name
        self.ds = VectorDataStore(vector_index_name)

    def init_all(self):
        self.ds.init_index()

    def _generate_id(self) -> str:
        return str(uuid.uuid4())

    def get_embeddings(self,txt):
       txt = self.pre_process(txt)
       logging.info("Calling openai to get text embedding")
       embeddings = get_embeddings([txt])
       return embeddings[0]

    def index_text(self,text,reference):
       id = self._generate_id()
       text = self.pre_process(text)
       embeddings = get_embeddings([text])
       reference_dict = {"reference":reference}
       self.ds.save_single(id,embeddings[0],reference_dict)
       
    def _retrieve_context_documents(self,query,top_k=5):
        query_emb = get_embeddings([query])
        return self.ds.search(query_emb[0],top_k)
    
    def answer(self,prompt_builder:PromptBuilder,query:str):
        results = self._retrieve_context_documents(query)
        matches = [{"reference": x['metadata']['reference'],
                "score": x['score']} for x in results['matches']
               ]
        print(matches)
        local_reference = matches[0]['reference']
        print(f"Local reference {local_reference}")
        context = self._read_context_file(local_reference)
        print(len(context))
        return chat_completation(prompt_builder.get_prompt(context,query))
    
    def _read_context_file(self,reference):
        directory = "./context"  # replace with the path to your directory
        with open(os.path.join(directory, reference), "r") as f:
            file_contents = f.read()
        return file_contents
    
    def delete_vindex_content(self):
       self.ds.delete_all()

