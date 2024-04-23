from .response import Response

class Round():

    def __init__(self, responses: list[Response]) -> None:
        
        self.responses = responses
        
        # TODO: Flagging mechanism

    def __str__(self):

        summary = f"{self.responses[0]}\n{self.responses[1]}\n{self.responses[2]}"
        return summary