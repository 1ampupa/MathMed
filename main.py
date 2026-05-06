import flet

from module.core.operators import Operators
from module.core.save_load import SaveLoad
from module.core.state import StateManager
from module.core.user import User
from module.core.session import Session

import module.gui.main_menu as app

# Debug Mode for each script
StateManager.debug_mode = True

# Create save folder if not exist
SaveLoad.create_core_folders()

app.flet.run(main=app.main_menu)

# user1 = User.create()

# session = Session(Operators.MULTIPLICATION)
# session.connect_user(user1)
# session.start()
