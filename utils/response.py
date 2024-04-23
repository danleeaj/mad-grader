from .model import Model
from datetime import datetime

class Response():

    def __init__(self, type: str, model: Model, content: str, time_requested: datetime,time_completed: datetime):

        self.type = type
        self.model = model
        self.content = content
        self.time_requested = time_requested
        self.time_completed = time_completed
        self.time_taken = time_completed - time_requested
    
    def __str__(self):

        summary = (
            f"     Response object from {self.type} of model {self.model.name}. " 
            f"Request initiated on {self.time_requested} and took {self.time_taken} to complete.\n"
            f"     Content Summary: {str(self.content)[:100]}..."
        )
        
        return summary