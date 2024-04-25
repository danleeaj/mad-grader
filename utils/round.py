from .response import Response

class Round():
    """
    Represents a single round of a debate, consisting of two Grader and one Evaluator response.

    Attributes:
        responses (list[Response]): A list of three responses from Grader 1, Grader 2 and the Evaluator.
        evaluation_error_flag (bool): Indicates mismatch between the individual Grader's evaluations and the Evaluator's determination of their agreement. For example, the Graders do not agree with each other, however, the Evaluator reports they do agree.
        consensus_error_flag (bool): Indicates mismatch between the Evaluator's consensus evaluation and the individual Grader's evaluations. For example, the Graders agree that the rubric component is satisfied, however, the Evaluator reports that the component was not satisfied.
    """

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
    
    def toJSON(self):

        return {
            "potentialEvaluationError?" : self.evaluation_error_flag,
            "potentialConsensusError?" : self.evaluation_error_flag,
            "responses" : {
                "graderResponse1" : self.responses[0].toJSON(),
                "graderResponse2" : self.responses[1].toJSON(),
                "evaluatorResponse" : self.responses[2].toJSON()
            }
        }