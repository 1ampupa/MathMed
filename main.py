from module.operator import Operator
from module.user import User
from module.user_answer import UserAnswer
from module.session import Session
from module.quiz import Quiz

Quiz.debug_mode = False

user = User(input("Enter your name: "))

print(f"Hi, {user.name}!")

session = Session()
session.connect_user(user)

print("Session is ready!\nAnswer the questions correctly.\n")

while True:
    quiz = Quiz.generate(user, Operator.MULTIPLICATION)
    print(quiz)

    answer = input("Answer for world peace: ")
    if answer.strip().lower() == 'q':
        session.disconnect_user()
        print("You quit the game. Thanks for saving world peace.")
        break
    
    try:
        result = UserAnswer(user, quiz, int(answer))
    except ValueError:
        print("Invalid input, please answer the question using only numbers.")
        continue
    diff_update = result.update_difficulty()

    print(f"{result}! The answer is {result.quiz.answer}.\n")
    