from module.operator import Operator
from module.user import User
from module.session import Session
from module.quiz import Quiz

# Debug Mode for each script
Quiz.debug_mode = False # Show quiz answer if true

user = User(input("Enter your name: "))

print(f"Hi, {user.name}!")

session = Session(Operator.MULTIPLICATION)
session.connect_user(user)
try:
    session.start()
except Exception as e:
    print(f"A fatal error occurred, and the session was ended unexpectedly with the following error message:\n{e}")
    input("Press enter button to exit.")
