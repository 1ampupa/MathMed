from module.core.utils.operators import Operators
from module.core.utils.save_load import SaveLoad
from module.core.utils.state import State, StateManager
from module.core.user.user import User
from module.core.session.session import Session

# Debug Mode for each script
StateManager.debug_mode = False

SaveLoad.create_core_folders()

user = User.create()

print(f"Hi, {user.name}!")

session = Session(Operators.MULTIPLICATION)
session.connect_user(user)
session.start()
