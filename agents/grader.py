from openai import OpenAI
import json

class Grader:
    
    def __init__(self, model_name: str="gpt-3.5-turbo-0125"):
        self.client = OpenAI()
        self.model_name = model_name
    
    def grade(self, rubric_component: str, student_response: str, grader_argument: str=None, context: str=None):
        message = [
          {"role": "system",
          "content": f"You are a biology grading assistant. Your task is to evaluate student responses{', as well as arguments from another grading assistant, ' if grader_argument else ' '}to determine if the rubric component is satisfied{', taking into account the information provided to the student in the context section' if context else ''}. You will provide your evaluation in JSON format."},
          {"role": "user",
          "content": f"""
          The rubric component is: '{rubric_component}'.
          The student response is: '{student_response}'.
          {'The context is: ' + f"'{context}'" if context else ''}
          {'The previous argument is: ' + f"'{grader_argument}'" if grader_argument else ''}
          Your job is to carefully read the response and determine if it explicitly expresses that the rubric component is fully satisfied. If there are no relevant responses, indicate that as well.
          Return your evaluation in JSON format with the following keys:
          'rubricComponentSatisfied': <'Yes'/'Partial'/'No'>
          'explanation' : <A string with a few sentences explaining your reasoning>
          """}
        ]

        completion = self.client.chat.completions.create(
          model=self.model_name, 
          response_format={"type": "json_object"},
          messages = message
        )

        response = json.loads(completion.choices[0].message.content)
        
        return response

