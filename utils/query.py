
from .model import Model

from typing import Any

from openai import OpenAI
import openai

import anthropic
from anthropic import _exceptions

import json

from .response import Response

from datetime import datetime

class APIError(Exception):
    pass

def query_gpt(model_name: str, message: str) -> Any:

    client = OpenAI()

    try:
        completion = client.chat.completions.create(
            model = model_name, 
            response_format = {"type": "json_object"},
            messages = message
        )
        
    except openai.APIConnectionError as e:
        print("Server could not be reached.")
        print(e.__cause__)
        raise APIError()
    except openai.RateLimitError as e:
        print("Too many requests.")
        raise APIError()
    except openai.APIStatusError as e:
        print(f"{e.status_code} Error.")
        print(e.response)
        raise APIError()

    return completion.choices[0].message.content



def query_claude(model_name: str, message: str) -> Any:

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
        raise APIError()
                
    return completion.content[0].text

def validate_json(response: dict, type: str):

    if type == "Evaluator":
        required_keys = ["gradersAgree", "consensusEvaluation", "explanation"]
    elif type == "Grader":
        required_keys = ["rubricComponentSatisfied", "explanation"]
    else:
        raise TypeError(f"Type {type} not 'Evaluator' or 'Grader'.")
    
    missing = []

    for key in required_keys:
        if key not in response:
            missing.append(key)
    
    return (len(missing) == 0)

def query(model: Model, message: str, type: str):

    model_name = model.value

    time_requested = datetime.now()

    try:

        match model.name:
            
            case "GPT":
                response = query_gpt(model_name, message)

            case "CLAUDE":
                response = query_claude(model_name, message)

            case _:
                raise ValueError("Model currently not supported. Either GPT or CLAUDE.")
            
    except APIError:

        raise APIError("Internal issue with API. Refer to previous error messages.")
    
    if response:

        max_retries = 3
        retry_count = 0

        while retry_count < max_retries:
            try:
                return_object = json.loads(response)
                if validate_json(return_object, type):
                    return Response(
                        type= type,
                        model= model,
                        content= return_object,
                        time_requested= time_requested,
                        time_completed= datetime.now()
                    )
                else:
                    raise json.JSONDecodeError("Failed to parse JSON due to invalid keys.")
            except json.JSONDecodeError:
                retries += 1

        raise APIError("Failed to parse JSON after multiple retries.")

