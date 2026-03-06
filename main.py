from module.operator import Operator
from module.quiz import Quiz
from module.difficulty_manager import DifficultyManager

Quiz.debug_mode = False

quiz1 = Quiz.generate(Operator.ADDITION)
print(quiz1)
quiz2 = Quiz.generate(Operator.SUBTRACTION)
print(quiz2)
quiz3 = Quiz.generate(Operator.MULTIPLICATION)
print(quiz3)
quiz4 = Quiz.generate(Operator.DIVISION)
print(quiz4)

# for _ in range(100):
# DifficultyManager.modify_difficulty(Operator.ADDITION, True)
