from .response import Response

class Round():

    def __init__(self, responses: list[Response]) -> None:
        
        self.responses: list[Response] = responses

        self.evaluation_error_flag: bool = (responses[0].content['rubricComponentSatisfied'] == responses[1].content['rubricComponentSatisfied']) != responses[2].content['gradersAgree']
        self.consensus_error_flag: bool = False

        if not self.evaluation_error_flag:

            if not responses[2].content['consensusEvaluation'] == 'No consensus reached':

                self.consensus_error_flag = (responses[0].content['rubricComponentSatisfied'] != responses[2].content['consensusEvaluation']) or (responses[1].content['rubricComponentSatisfied'] != responses[2].content['consensusEvaluation'])
        
    def __str__(self):

        summary = f"Round object.{' Flagged.' if self.evaluation_error_flag or self.consensus_error_flag else ''}\n\n{self.responses[0]}\n\n{self.responses[1]}\n\n{self.responses[2]}\n"
        return summary