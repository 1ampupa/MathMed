from module.core.operators import Operators
from module.core.save_load import SaveLoad
from module.core.state import StateManager
from module.core.user import User
from module.core.session import Session

# Debug Mode for each script
StateManager.debug_mode = False

# Create save folder if not exist
SaveLoad.create_core_folders()

user1 = User.create()

print(f"Hi, {user1.name}!")

session = Session(Operators.MULTIPLICATION)
session.connect_user(user1)
session.start()
