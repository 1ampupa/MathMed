from module.operator import Operator
from module.quiz import Quiz
from module.user import User
from module.user_answer import UserAnswer

Quiz.debug_mode = False

user_name = input("Enter your name: ")
user = User(user_name)

print(f"Hi, {user.name}!")
while True:
    quiz = Quiz.generate(user, Operator.MULTIPLICATION)
    print(quiz)

    answer = input("Answer for world peace: ")
    if answer == "q": break

    result = UserAnswer(user, quiz, int(answer))
    diff_update = result.update_difficulty()

    print(f"{result}! The answer is {result.quiz.answer}.\n")
