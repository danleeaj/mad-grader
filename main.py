from agents.grader import Grader
from agents.evaluator import Evaluator

grader1 = Grader()
grader2 = Grader()

evaluator = Evaluator()

consensus = False
rounds = 0

rubric_component = "Testosterone suppresses LH production, GnRH production, hypothalamic function or anterior pituitary function."

student_response = "Her LH levels would decrease because of testosterone would stop the positive feedback caused by "

context = """
Many transgender men choose to take testosterone as part of their gender transition. You are a doctor who is supervising the medical treatment of a particular individual who wants to start taking testosterone. This is what you know so far:

- The patient is an adult with **typically functioning ovaries and uterus**.
- For now, the patient will **not** have any surgeries, and the **only** medication taken is the testosterone.
- The patient will be given high levels of testosterone, as compared to typical levels in cisgender (non-transgender) women.
- In people with ovaries, the hypothalamus and anterior pituitary have testosterone receptors. The amount of testosterone given to the patient will be high enough to make the hypothalamus and the anterior pituitary change their hormone secretion in the same way as these structures would respond to high levels of testosterone in cisgender men.
"""

while not consensus:
    grader1_argument = grader1.grade(rubric_component, student_response, context=context)
    grader2_argument = grader2.grade(rubric_component, student_response, context=context)
    print(grader1_argument)
    print(grader2_argument)
    evaluation = evaluator.evaluate(grader1_argument, grader2_argument)
    print(evaluation)
    consensus = True if evaluation['gradersAgree'] == True else False