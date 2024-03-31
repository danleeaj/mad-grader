import openai
from openai import OpenAI
import json

class Evaluator:
    
    def __init__(self, model_name: str="gpt-3.5-turbo-0125"):
        self.client = OpenAI()
        self.model_name = model_name
    
    def evaluate(self, grader1_response: str, grader2_response: str):
        message = [
          {"role": "system",
          "content": "You are a grading judge. Your task is to evaluate the grading responses from two grading agents to determine if they agree on whether a rubric component is satisfied by the student response. You will provide your evaluation in JSON format."},
          {"role": "user",
          "content": f"""
          Grader 1 evaluation: '{grader1_response}'.
          Grader 2 evaluation: '{grader2_response}'.
          Your job is to compare the evaluations from Grader 1 and Grader 2. If their evaluations on whether the rubric component is satisfied (YES), not satisfied (NO) or partially satisfied (PARTIAL) are in agreement with each other, then provide their consensus evaluation and say that they agree by evaluating gradersAgree as TRUE. If the two graders still reach the same conclusions for different reasons, return true for gradersAgree.
          However, if the two graders disagree in their evaluations (one says YES and the other says NO, or one says PARTIAL and the other says either YES or NO), then evaluate gradersAgree as FALSE and say 'No consensus reached' for consensusEvaluation.
          Return your evaluation in JSON format with the following keys:
          'gradersAgree' : <true/false>
          'consensusEvaluation': <'Yes'/'No'/'Partial'/'No consensus reached'>
          'explanation' : <A string with a few sentences explaining your reasoning>
          """}
        ]

        try:
          completion = self.client.chat.completions.create(
            model=self.model_name, 
            response_format={"type": "json_object"},
            messages = message
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
        
        return response


