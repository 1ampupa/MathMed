from module.core.operator import Operator
from module.core.state import State, StateManager
from module.core.user import User
from module.core.session import Session
from module.core.quiz import Quiz

# Debug Mode for each script
StateManager.debug_mode = False

user = User(input("Enter your name: "))

print(f"Hi, {user.name}!")

session = Session(Operator.MULTIPLICATION)
session.connect_user(user)
session.start()
