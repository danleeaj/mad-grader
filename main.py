from agents.grader import Grader
from agents.evaluator import Evaluator

from utils import Model

context = """
In a healthy person without diabetes, are insulin levels regulated homeostatically? (Note: we are referring to levels of the hormone insulin, not to blood sugar levels.) Refer to at least one element of the homeostatic circuit to justify your response.
"""

# rubric_component = "No setpoint for insulin / levels vary"

rubric_component = "Mentioning any element of the homeostatic circuit (setpoint, sensor, control center, effector)"

student_response = "No because there is no setpoint for insulin levels. Typically, levels of insulin rise and fall depending on when and what one has eaten and one’s blood sugar level instead of staying at a fixed level."

def debate(rubric_component, student_response, context: str = None):
    
    grader1 = Grader(Model.GPT)
    grader2 = Grader(Model.CLAUDE)
    evaluator = Evaluator(Model.CLAUDE)
    
    grader1.setup_message(rubric_component, student_response, context)
    grader1_argument = grader1.evaluate()
    grader2.setup_message(rubric_component, student_response, context)
    grader2_argument = grader2.evaluate()

    evaluator.setup_message(grader1_argument, grader2_argument)
    evaluator_argument = evaluator.evaluate()

    print(f"GRADER 1 ARGUMENT -------- \n\n{grader1_argument} \n\nGRADER 2 ARGUMENT -------- \n\n{grader2_argument} \n\nEVALUATION --------------- \n\n{evaluator_argument} \n\n")

    while not evaluator_argument['gradersAgree']:
    # while not grader1_argument['rubricComponentSatisfied'] == grader2_argument['rubricComponentSatisfied']:

        grader1.add_argument(grader2_argument)
        grader2.add_argument(grader1_argument)
        grader1_argument = grader1.evaluate()
        grader2_argument = grader2.evaluate()

        evaluator.setup_message(grader1_argument, grader2_argument)
        evaluator_argument = evaluator.evaluate()

        print(f"GRADER 1 ARGUMENT -------- \n{grader1_argument} \n\nGRADER 2 ARGUMENT -------- \n{grader2_argument} \n\nEVALUATION --------------- \n{evaluator_argument} \n\n")
    
    print("FINISH ------------------")

if __name__ == "__main__":
    debate(rubric_component, student_response, context)