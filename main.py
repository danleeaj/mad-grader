from agents.grader import Grader
from agents.evaluator import Evaluator

from utils.utils import Model, stopwatch

import concurrent.futures

from itertools import repeat

context = ""

rubric_component = "High blood pressure and diabetes often go together"

student_response = "The connection between high blood pressure and diabetes is not due to angiotensin II decreasing GLUT4. Instead, angiotensin II actually increases the amount of GLUT4 in the cell membrane, which would help improve glucose uptake and regulate blood sugar levels."

# TODO: Implement response class and refactor the code so that debate returns multiple response objects instead of a huge ass json.

# @stopwatch
def debate(rubric_component, student_response, context: str = None):

    debate_history = []
    round_history = {}

    grader1 = Grader(Model.GPT)
    grader2 = Grader(Model.CLAUDE)
    evaluator = Evaluator(Model.CLAUDE)
    
    grader1.setup_message(rubric_component, student_response, context)
    # grader1_argument = grader1.evaluate()

    grader2.setup_message(rubric_component, student_response, context)
    # grader2_argument = grader2.evaluate()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        t1 = executor.submit(grader1.evaluate)
        t2 = executor.submit(grader2.evaluate)

        grader1_argument = t1.result()
        grader2_argument = t2.result()

    evaluator.setup_message(grader1_argument, grader2_argument)
    evaluator_argument = evaluator.evaluate()
    round_history['Grader 1'], round_history['Grader 2'], round_history['Evaluator'] = grader1_argument, grader2_argument, evaluator_argument
    debate_history.append(round_history)

    # print(f"{"GRADER 1 ARGUMENT ":-<100} \n{round_history['Grader 1']} \n\n{"GRADER 2 ARGUMENT ":-<100} \n{round_history['Grader 2']} \n{"EVALUATION ":-<100} \n{round_history['Evaluator']} \n\n")

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

        # print(f"{"GRADER 1 ARGUMENT ":-<100} \n{round_history['Grader 1']} \n\n{"GRADER 2 ARGUMENT ":-<100} \n{round_history['Grader 2']} \n\n{"EVALUATION ":-<100} \n{round_history['Evaluator']} \n\n")
    
    print("FINISH ------------------")

    return debate_history



if __name__ == "__main__":
    # start = time.perf_counter()
    # debate(rubric_component, student_response, context)
    response = debate(rubric_component, student_response, context)

    for component in response:
        print(component)

        for dialog in response[component]:
            print(dialog)
    # end = time.perf_counter()


# # @stopwatch
# def debate_rubric_set(rubric_components: list[str], student_response: str, context: str):

#     breakdown = {}
    
#     with concurrent.futures.ThreadPoolExecutor() as executor:
#         results = executor.map(debate, rubric_components, repeat(student_response, len(rubric_components)), repeat(context, len(rubric_components)))

#         for i, result in enumerate(results):
#             breakdown[rubric_components[i]] = result
    
#     # print(breakdown)

#     return breakdown

#         # for i in range(len(results)):
#         #     breakdown[rubric_components[i]] = results[i]