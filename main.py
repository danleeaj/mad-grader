from agents.grader import Grader
from agents.evaluator import Evaluator

from utils.round import Round

from utils.query import Model
from utils.utils import stopwatch

import concurrent.futures

from itertools import repeat

context = ""

rubric_component = "High blood pressure and diabetes often go together"

student_response = "The connection between high blood pressure and diabetes is not due to angiotensin II decreasing GLUT4. Instead, angiotensin II actually increases the amount of GLUT4 in the cell membrane, which would help improve glucose uptake and regulate blood sugar levels."

# TODO: Implement response class and refactor the code so that debate returns multiple response objects instead of a huge ass json.
# TODO: Implement Round() and Debate() classes as well


# @stopwatch
def debate(rubric_component, student_response, context: str = None):

    debate_history = []

    grader1 = Grader(Model.GPT)
    grader2 = Grader(Model.CLAUDE)
    evaluator = Evaluator(Model.CLAUDE)
    
    grader1.setup_message(rubric_component, student_response, context)

    grader2.setup_message(rubric_component, student_response, context)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        t1 = executor.submit(grader1.evaluate)
        t2 = executor.submit(grader2.evaluate)

        grader1_argument = t1.result()
        grader2_argument = t2.result()

    evaluator.setup_message(grader1_argument.content, grader2_argument.content)
    evaluator_argument = evaluator.evaluate()

    round = Round([grader1_argument, grader2_argument, evaluator_argument])

    print(round)

    # TODO: Figure out __str__ method for both Round() and Response() so that it makes sense.
    # TODO: Implement Debate() object.

    while not evaluator_argument.content['gradersAgree']:

        grader1.add_argument(grader2_argument.content)
        grader2.add_argument(grader1_argument.content)

        with concurrent.futures.ThreadPoolExecutor() as t:
            t1 = t.submit(grader1.evaluate)
            t2 = t.submit(grader2.evaluate)

            grader1_argument = t1.result()
            grader2_argument = t2.result()

        evaluator.setup_message(grader1_argument.content, grader2_argument.content)
        evaluator_argument = evaluator.evaluate()

        round = Round([grader1_argument, grader2_argument, evaluator_argument])

        print(round)

    return debate_history


if __name__ == "__main__":

    response = debate(rubric_component, student_response, context)
    print(response)
