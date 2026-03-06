from module.operator import Operator
from module.quiz import Quiz
from module.user_answer import User
from module.user_answer import UserAnswer

Quiz.debug_mode = False

user = User("Test User")

print(f"Hi, {user.name}!")
while True:
    quiz = Quiz.generate(Operator.ADDITION)
    print(quiz)

    answer = int(input("Answer for world peace: "))

    result = UserAnswer(user, quiz, answer)

    print(result)
    # print(user.difficulty_chart[quiz.operator])
