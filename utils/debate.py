# TODO: Implement debate class.

from .round import Round

class Debate():

    def __init__(self, rubric_component: str, student_response: str, context: str = None) -> None:
        self.rubric_component = rubric_component
        self.student_response = student_response
        self.context = context
        self.rounds = []
        self.round_count = len(self.rounds) + 1

    def add_round(self, round: Round) -> None:
        self.rounds.append(round)

    def __str__(self) -> str:
        
        summary = f"Debate object for rubric component '{self.rubric_component[:50]}...' with student response '{self.student_response[:50]}...'. {self.round_count} round(s) of debate took place."

        return summary