from agents.grader import Grader
from agents.evaluator import Evaluator

grader1 = Grader()
grader2 = Grader()

evaluator = Evaluator()

consensus = False
rounds = 0

rubric_component = "Testosterone suppresses LH production, GnRH production, hypothalamic function or anterior pituitary function."

student_response = "Her LH levels would decrease because of testosterone would stop the positive feedback caused by "

while not consensus:
    grader1_argument = grader1.grade(rubric_component, student_response)
    grader2_argument = grader2.grade(rubric_component, student_response)
    print(grader1_argument)
    print(grader2_argument)
    evaluation = evaluator.evaluate(grader1_argument, grader2_argument)
    print(evaluation)
    consensus = True if grader1_argument['rubricComponentSatisfied'] == grader2_argument['rubricComponentSatisfied'] else False