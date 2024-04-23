from .response import Response

class Round():

    def __init__(self) -> None:
        
        self.responses = []

    def add_response(self, responses: list[Response]):

        self.responses = responses