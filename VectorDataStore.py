
import pinecone
import config.SystemConfig as cfg
import logging

'''
Main class to interact with the Vector Database.

This implementation is specific to the Pinecone Vector Database.

'''
class VectorDataStore:

    def __init__(self,index_name:str) -> None:
        self.key        = cfg.pinecone_api_key
        self.index_name = index_name

    def init_index(self):

        pinecone.init(
            api_key     = self.key, 
            environment = cfg.pinecone_env
            )
        
        # check if index already exists.
        if self.index_name not in pinecone.list_indexes():
           # if does not exist, create index
           pinecone.create_index(
             self.index_name,
             dimension = cfg.VECTOR_DIMENSIONS,
             metric    = 'cosine',
             metadata_config={'indexed': ['reference']}
           )

    
        # connect to index
        self.index = pinecone.Index(self.index_name)
        logging.info(f'Connected to index {self.index_name}')

   

    def save_single(self,id,embedding:list,reference_dict):
        
        if (embedding==None):
            logging.warning('Embeddings is mandatory for save operation')
            return 
            
        record = (id ,embedding, reference_dict)
        self.index.upsert([record])

    def save_batch(self,ids_batch,embeddings,meta_batch):
        if (embeddings==None):
            logging.warning('Embeddings is mandatory for batch save operation')
            return 
        
        if (ids_batch==None):
            logging.warning('ids_batch is mandatory for batch save operation')
            return 
        
        if (meta_batch==None):
            logging.warning('metadata batch is mandatory for batch save operation')
            return 

        to_upsert = list(zip(ids_batch, embeddings, meta_batch))
        self.index.upsert(to_upsert)

    def search(self,qry,top_k=5):
        
        if (qry==None):
            logging.warning('Query Embeddings is mandatory for index search')
            return None

        results = self.index.query(qry,top_k=top_k,include_metadata=True)
        return results
    
    def delete_all(self):
        # Delete all items in the index
        self.index.delete(deleteAll='true')


