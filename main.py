from module.operator import Operator
from module.user import User
from module.session import Session
from module.quiz import Quiz

Quiz.debug_mode = False

user = User(input("Enter your name: "))

print(f"Hi, {user.name}!")

session = Session(Operator.ADDITION)
session.connect_user(user)
session.start()
