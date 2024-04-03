from enum import Enum

from openai import OpenAI
import openai

import json

# TODO: Add enum for different models.

class Model(Enum):
    GPT = "gpt-3.5-turbo-0125"
    GEMINI = "gemini-pro"
    CLAUDE = "claude-3-haiku-20240307"

# TODO: Error handling -> invalid model results in AttributeError

# TODO: Implement support for multiple models.
    
def query(model: Model, message: str):

    model_name = model.value

    match model.name:
        case "GPT":

            client = OpenAI()

            try:
                completion = client.chat.completions.create(
                    model = model_name, 
                    response_format = {"type": "json_object"},
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

        case "CLAUDE":
            print("CLAUDE")
        case "GEMINI":
            print("GEMINI")
        case _:
            print("Working on it!")

