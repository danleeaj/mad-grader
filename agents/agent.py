from utils import Model, query

# TODO: Make sure that the request is also added to the message history.
# TODO: Implement support for multiple models (use enum)

class Agent:

	def __init__(self):
		self.message = []

	def update_message(self, m):
		"""Updates message to keep track of the entire conversation.

		Args:
		m -- the message intended to be added to the conversation history.
		"""
		for dialog in m:
			self.message.append(dialog)
      
	def evaluate(self, model: Model) -> str:
		"""Makes API call to respective LLM model with error handling. Automatically appends request and response to message history.

		Args:
			model (Model): The LLM model to use for generating responses.

		Returns:
			str: The .json response generated by the model.
		"""

		response = query(model, self.message)

		self.message.append({
			"role": "assistant", 
			"content" : response
		})
		
		return response