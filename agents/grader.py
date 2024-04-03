from .agent import Agent

class Grader(Agent):
		
	def __init__(self, model_name: str="gpt-3.5-turbo-0125"):
		super().__init__(model_name)
		self.count = 0
	
	def evaluate(self):
		self.count += 1
		return super().evaluate()
	
	def setup_message(self, rubric_component: str, student_response: str, context: str=None):
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

	def add_argument(self, argument):
		message = [
			{"role": "user",
			"content": argument}
		]
		super().update_message(message)
