from .agent import Agent

class Evaluator(Agent):
	def __init__(self):
		super().__init__()
	
	def setup_message(self, grader1_response, grader2_response):
		initial_message = [
			{"role": "system",
			"content": "You are a grading judge. Your task is to evaluate the grading responses from two grading agents to determine if they agree on whether a rubric component is satisfied by the student response. You will provide your evaluation in JSON format."},
			{"role": "user",
			"content": f"""
			Grader 1 evaluation: '{grader1_response}'.
			Grader 2 evaluation: '{grader2_response}'.
			Your job is to compare the evaluations from Grader 1 and Grader 2. If their evaluations on whether the rubric component is satisfied (YES) or not satisfied (NO) are in agreement with each other, then provide their consensus evaluation and say that they agree by evaluating gradersAgree as TRUE.
			To determine if the graders are in agreement, follow these rules:
			1. If both graders provide the same evaluation (YES or NO), they are considered to be in agreement.
			2. If the graders provide different evaluations (one says YES and the other says NO), then they are considered to be in disagreement.
			3. If the graders provide the same evaluations, but for very different reasons, then they are also considered to be in disagreement.
			However, if the two graders disagree in their evaluations (one says YES and the other says NO), then evaluate gradersAgree as FALSE and say 'No consensus reached' for consensusEvaluation.
			Return your evaluation in JSON format with the following keys:
			'gradersAgree' : <true/false>
			'consensusEvaluation': <'Yes'/'No'/'No consensus reached'>
			'explanation' : <A string with a few sentences explaining your reasoning>
			"""}
		]
		super().update_message(initial_message)




