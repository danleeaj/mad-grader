from openai import OpenAI
import openai
import json

class Agent:

	def __init__(self, model_name: str="gpt-3.5-turbo-0125"):
		self.client = OpenAI()
		self.model_name = model_name
		self.message = []

	def update_message(self, m):
		for dialog in m:
			self.message.append(dialog)
      
	def evaluate(self):
		try:
			completion = self.client.chat.completions.create(
				model=self.model_name, 
				response_format={"type": "json_object"},
				messages = self.message
			)
			response = json.loads(completion.choices[0].message.content)
			
		except openai.APIConnectionError as e:
			print("Server could not be reached.")
			print(e.__cause__)
		except openai.RateLimitError as e:
			print("Too many requests.")
		except openai.APIStatusError as e:
			print(f"{e.status_code} Error.")
			print(e.response)
		
		self.message.append({
			"role": "assistant", 
			"content" : response
		})
		
		return response