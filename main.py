from agents.grader import Grader
from agents.evaluator import Evaluator

from utils import Model

grader1 = Grader()
grader2 = Grader()

evaluator = Evaluator()

consensus = False
rounds = 0

context = """
In a healthy person without diabetes, are insulin levels regulated homeostatically? (Note: we are referring to levels of the hormone insulin, not to blood sugar levels.) Refer to at least one element of the homeostatic circuit to justify your response.
"""

rubric_component = "No setpoint for insulin / levels vary"

student_response = "No because there is no setpoint for insulin levels. Typically, levels of insulin rise and fall depending on when and what one has eaten and one’s blood sugar level instead of staying at a fixed level."

grader1.setup_message(rubric_component, student_response, context)
grader1_argument = grader1.evaluate(Model.GPT)
print(grader1_argument)

grader2.setup_message(rubric_component, student_response, context)
grader2_argument = grader2.evaluate(Model.CLAUDE)
print(grader2_argument)

evaluator.setup_message(grader1_argument, grader2_argument)
evaluator_argument = evaluator.evaluate(Model.CLAUDE)
print(evaluator_argument)

# while not consensus:

#     grader1.setup_message(rubric_component, student_response, context)
#     grader1_argument = grader1.grade()
#     print(grader1_argument)

#     grader1_argument = grader1.grade(rubric_component, student_response, context)
#     print(grader1_argument)

#     grader2_argument = grader2.grade(rubric_component, student_response, context=context)
#     print(grader2_argument)

#     evaluation = evaluator.evaluate(grader1_argument, grader2_argument)
#     print(evaluation)

#     consensus = True if evaluation['gradersAgree'] == True else False

#     grader1.add_argument(grader2_argument)
#     grader2.add_argument(grader1_argument)

