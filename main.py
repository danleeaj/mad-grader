from agents.grader import Grader
from agents.evaluator import Evaluator

from utils import Model

import concurrent.futures

import time

context = """
In a healthy person without diabetes, are insulin levels regulated homeostatically? (Note: we are referring to levels of the hormone insulin, not to blood sugar levels.) Refer to at least one element of the homeostatic circuit to justify your response.
"""

rubric_component = "No setpoint for insulin / levels vary"

# rubric_component = "Mentioning any element of the homeostatic circuit (setpoint, sensor, control center, effector)"

student_response = "No because there is no setpoint for insulin levels. Typically, levels of insulin rise and fall depending on when and what one has eaten and one’s blood sugar level instead of staying at a fixed level."

def debate(rubric_component, student_response, context: str = None):

    debate_history = []
    round_history = {}

    grader1 = Grader(Model.GPT)
    grader2 = Grader(Model.GPT)
    evaluator = Evaluator(Model.GPT)
    
    grader1.setup_message(rubric_component, student_response, context)
    # grader1_argument = grader1.evaluate()

    grader2.setup_message(rubric_component, student_response, context)
    # grader2_argument = grader2.evaluate()

    with concurrent.futures.ThreadPoolExecutor() as t:
        t1 = t.submit(grader1.evaluate)
        t2 = t.submit(grader2.evaluate)

        grader1_argument = t1.result()
        grader2_argument = t2.result()

    evaluator.setup_message(grader1_argument, grader2_argument)
    evaluator_argument = evaluator.evaluate()
    round_history['Grader 1'], round_history['Grader 2'], round_history['Evaluator'] = grader1_argument, grader2_argument, evaluator_argument
    debate_history.append(round_history)

    print(f"{"GRADER 1 ARGUMENT ":-<100} \n{round_history['Grader 1']} \n\n{"GRADER 2 ARGUMENT ":-<100} \n{round_history['Grader 2']} \n\{"EVALUATION ":-<100} \n{round_history['Evaluator']} \n\n")

    while not evaluator_argument['gradersAgree']:
    # while not grader1_argument['rubricComponentSatisfied'] == grader2_argument['rubricComponentSatisfied']:

        grader1.add_argument(grader2_argument)
        grader2.add_argument(grader1_argument)

        with concurrent.futures.ThreadPoolExecutor() as t:
            t1 = t.submit(grader1.evaluate)
            t2 = t.submit(grader2.evaluate)

            grader1_argument = t1.result()
            grader2_argument = t2.result()

        # grader1_argument = grader1.evaluate()
        # grader2_argument = grader2.evaluate()

        evaluator.setup_message(grader1_argument, grader2_argument)
        evaluator_argument = evaluator.evaluate()

        round_history['Grader 1'], round_history['Grader 2'], round_history['Evaluator'] = grader1_argument, grader2_argument, evaluator_argument
        debate_history.append(round_history)

        print(f"{"GRADER 1 ARGUMENT ":-<100} \n{round_history['Grader 1']} \n\n{"GRADER 2 ARGUMENT ":-<100} \n{round_history['Grader 2']} \n\n{"EVALUATION ":-<100} \n{round_history['Evaluator']} \n\n")
    
    print("FINISH ------------------")

    return debate_history

if __name__ == "__main__":
    # start = time.perf_counter()
    debate(rubric_component, student_response, context)
    # end = time.perf_counter()