from .model import Model

class Response():

    def __init__(self, type: str, model: Model, content: str, time_completed: str):
        
        self.type = type
        self.model = model
        self.content = content
        self.time_completed = time_completed