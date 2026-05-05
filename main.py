from module.core.operators import Operators
from module.core.save_load import SaveLoad
from module.core.state import State, StateManager
from module.core.user import User
from module.core.session import Session

# Debug Mode for each script
StateManager.debug_mode = False

SaveLoad.create_core_folders()

user = User.create()

print(f"Hi, {user.name}!")

session = Session(Operators.MULTIPLICATION)
session.connect_user(user)
session.start()
