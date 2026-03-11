from module.core.operator import Operator
from module.core.user import User
from module.core.session import Session
from module.core.quiz import Quiz

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
