import os

class PromptBuilder():

    def __init__(self):
        pass

    def get_prompt(self,context:str,query:str):
        return ""
    
'''
Clase utilitaria para construir un prompt con el objetivo de responder
preguntas sobre programas de gobierno
'''
class PoliticAssistantPromptBuilder(PromptBuilder):

    def __init__(self):
        directory = "./context"
        filename = "politics.prompt.end.txt"
        self.prompt_end = self.load_file(os.path.join(directory, filename))

    def load_file(self,filepath):
        print(filepath)
        with open(filepath, "r") as f:
            file_contents = f.read()
        return file_contents
        

    def get_prompt(self,context:str,query:str):
        prompt = "Propuesta: \n\n" + context + self.prompt_end + query
        return prompt

