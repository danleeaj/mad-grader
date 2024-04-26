from .model import Model
from datetime import datetime

class Response():
    """
    Represents a single response generated by an LLM during a debate.

    Attributes:
        type (str): The type of agent sending the response (either 'Evaluator' or 'Grader').
        model (Model): The model of said agent.
        content (str): The content of the response in JSON.
        time_requested (datetime): The timestamp when the response is generated.
        time_completed (datetime): The timestamp when the response was completed.
        time_taken (datetime.timedelta): The time it took for the response to process.
    """

    def __init__(self, type: str, model: str, content: str, time_requested: datetime,time_completed: datetime):

        self.type = type
        self.model = model.name
        self.content = content
        self.time_requested = time_requested
        self.time_completed = time_completed
        self.time_taken = time_completed - time_requested
    
    def toJSON(self):

        return {
            "content" : self.content,
            "model" : self.model,
            "timeInitiated" : self.time_requested,#.strftime("%m/%d/%Y, %H:%M:%S"),
            "timeTaken" : str(self.time_taken)
        }
    
    def __str__(self):

        summary = (
            f"Response object from {self.type} of model {self.model}. " 
            f"Request initiated on {self.time_requested} and took {self.time_taken} to complete.\n"
            f"Content Summary: {str(self.content)[:100]}..."
        )
        
        return summary