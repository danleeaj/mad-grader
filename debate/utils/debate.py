# TODO: Implement debate class.

from .round import Round

class Debate():
    """
    Represents a complete debate process for a specific student response based on a rubric component.

    Attributes:
        rubric_component (str): The rubric component the debate is based off of.
        student_response (str): The student response being evaluated.
        context (str): Additional context for the evaluation.
        rounds (list[Round]): A list of all rounds of debate that took place.
        round_count (int): The number of rounds that took place.
        flagged (bool): Indicates potential error in evaluator evaluation.
        evaluation (bool): The final verdict on whether the rubric component is satisfied.
    """

    def __init__(self, rubric_component: str, student_response: str, context: str = None) -> None:
        self.rubric_component = rubric_component
        self.student_response = student_response
        self.context = context
        self.rounds = []
        self.round_count = len(self.rounds) + 1
        self.flagged: bool = False
        self.evaluation: bool = None

    def add_round(self, round: Round) -> None:
        self.rounds.append(round)
        if round.consensus_error_flag or round.evaluation_error_flag:
            self.flagged = True
    
    def complete_debate(self) -> None:
        self.evaluation = True if self.rounds[-1].responses[-1].content['consensusEvaluation'] == 'Yes' else False

    def __str__(self) -> str:
        
        summary = f"Debate object for rubric component '{self.rubric_component[:50]}...' with student response '{self.student_response[:50]}...'. {self.round_count} round(s) of debate took place. Rubric component satisfied yields {self.evaluation}."

        return summary