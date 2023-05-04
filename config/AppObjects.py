from Coordinator import Coordinator 

global coordinator

def init_coordinator(vector_index_name):
   global coordinator

   coordinator = Coordinator(vector_index_name)
   coordinator.init_all()
