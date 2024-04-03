from .agent import Agent

from utils import Model

class Grader(Agent):
		
	def __init__(self):
		super().__init__()
		self.count = 0
	
	def evaluate(self, model: Model):
		self.count += 1
		return super().evaluate(model)
	
	def setup_message(self, rubric_component: str, student_response: str, context: str=None):
		"""Updates message array prior to API query to add initial system and user queries.

		Args:
			rubric_component: The rubric component that the grader's evaluation should be based on.
			student_response: The response from the student that the grader should grade.
			context: The context of the question, such as the question itself, or important points that should be clarified for the grader.

		Returns:
			nil
		"""
		initial_message = [
			{"role": "system",
			"content": f"You are a biology grading assistant. Your task is to evaluate student responses to determine if the rubric component is satisfied{', taking into account the information provided to the student in the context section' if context else ''}. You will provide your evaluation in JSON format."},
			{"role": "user",
			"content": f"""
			The rubric component is: '{rubric_component}'.
			The student response is: '{student_response}'.
			{'The context is: ' + f"'{context}'" if context else ''}
			Your job is to carefully read the response and determine if it explicitly expresses that the rubric component is satisfied. If there are no relevant responses, indicate that as well.
			Return your evaluation in JSON format with the following keys:
			'rubricComponentSatisfied': <'Yes'/'No'>
			'explanation' : <A string with a few sentences explaining your reasoning>
			"""}
		]
		for dialog in initial_message:
			self.message.append(dialog)

	def add_argument(self, argument: str):
		"""Updates message array to inform the grader of the response made by the other grader.

		Args:
			argument: The argument made by the opposing grader that the grader should take into consideration before revaluating its evaluation.
		
		Returns:
			nil
		"""
		message = [
			{"role": "user",
			"content": argument}
		]
		super().update_message(message)
