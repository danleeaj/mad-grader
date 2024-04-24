from agents.grader import Grader
from agents.evaluator import Evaluator

from utils.round import Round
from utils.debate import Debate

from utils.query import Model
from utils.utils import stopwatch

import concurrent.futures

from itertools import repeat

import json

context = ""

rubric_component = "Amyloid beta plaques and neurofibrillary tangles are hallmarks of Alzheimer's."

student_response = "The histopathological hallmarks of Alzheimer's include amyloid beta plaque build-up and tau neurofibrillary tangle formation. They cause GluA2 receptor loss through causing receptor endocytosis."

# @stopwatch
def debate(rubric_component, student_response, context: str = None, grader1_model: Model = Model.GPT, grader2_model: Model = Model.CLAUDE, evaluator_model: Model = Model.CLAUDE, jsonify: bool = False) -> Debate:
    """
    Conducts a multi-round debate between two Grader models, facilitated by an Evaluator model.

    Args:
        rubric_component (str): The rubric component the debate is based off of.
        student_response (str): The student response being evaluated.
        context (str, optional): Additional context for the evaluation. Defaults to None.
        grader1_model (Model, optional): LLM model for the first grader. Defaults to Model.GPT.
        grader2_model (Model, optional): LLM model for the second grader. Defaults to Model.CLAUDE.
        evaluator_model (Model, optional): LLM model for the evaluator. Defaults to Model.CLAUDE.

    Returns:
        Debate: A Debate object containing the rounds of the argument and its final outcome.
    """
    
    debate_history = Debate(
        rubric_component=rubric_component,
        student_response=student_response,
        context=context
    )

    grader1 = Grader(grader1_model)
    grader2 = Grader(grader2_model)
    evaluator = Evaluator(evaluator_model)
    
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

    debate_history.add_round(round)

    print(round)

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

        debate_history.add_round(round)

        print(round)

    debate_history.complete_debate()

    if jsonify:
        return json.dumps(debate_history.toJSON(), default=str)

    return debate_history


if __name__ == "__main__":

    response = debate(rubric_component, student_response, context, jsonify=True)

    print(response)
    # print(json.dumps(response))