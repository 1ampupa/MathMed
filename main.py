from module.quiz import Quiz
from module.operator import Operator

Quiz.debug_mode = False

quiz1 = Quiz.generate(Operator.ADDITION)
print(quiz1)
quiz2 = Quiz.generate(Operator.SUBTRACTION)
print(quiz2)
quiz3 = Quiz.generate(Operator.MULTIPLICATION)
print(quiz3)
quiz4 = Quiz.generate(Operator.DIVISION)
print(quiz4)
