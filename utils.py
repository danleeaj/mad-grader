from enum import Enum

import sys

from openai import OpenAI
import openai

import anthropic
from anthropic import _exceptions

import json

# import google.generativeai as genai

import time
from functools import wraps

def stopwatch(func):
    """A decorator that prints the time taken by the decorated function.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Function {func.__name__} took {end_time - start_time:.6f} seconds to execute.")
        return result
    return wrapper

class Model(Enum):
    GPT = "gpt-3.5-turbo-0125"
    GEMINI = "gemini-pro"
    CLAUDE = "claude-3-haiku-20240307"

# TODO: Implement better error handling for the functions that call query() to catch.
    
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
                # print("----------", completion, "----------", sep="\n")
                response = json.loads(completion.choices[0].message.content)
                
            except openai.APIConnectionError as e:
                print("Server could not be reached.")
                print(e.__cause__)
                sys.exit()
            except openai.RateLimitError as e:
                print("Too many requests.")
                sys.exit()
            except openai.APIStatusError as e:
                print(f"{e.status_code} Error.")
                print(e.response)
                sys.exit()

            return response

        case "CLAUDE":
            
            client = anthropic.Anthropic()

            try:
                completion = client.messages.create(
                    model = model_name,
                    max_tokens = 1000,
                    temperature = 0.0,
                    system = message[0]['content'],
                    messages = message[1:]
                )
                # print("----------", completion, "----------", sep="\n")
            except Exception as e:
                print(f"Unexpected error: {e}")
                sys.exit()
                        
            response = json.loads(completion.content[0].text)
            return response

# TODO: Implement an error handling mechanism that ensures that the JSON returned is parsable, and reprompts in the case it isn't.

            # try:
            #     response = json.loads(completion.content[0].text)
            # except json.decoder.JSONDecodeError: 

# TODO: Implement support for Gemini. Refer to test.py for an example API call.

        # case "GEMINI":

        #     genai.configure()
        #     model = genai.GenerativeModel(model_name=model_name)

        #     for dialog in message:
        #         ...

        #     print("GEMINI")

# TODO: Preferably include support for other models that are cheaper and free. Becuase I am cheap.

        case _:
            raise ValueError("Model currently not supported. Either GPT or CLAUDE.")

