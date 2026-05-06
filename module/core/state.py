from enum import Enum, auto

class State(Enum):
    
    MAIN_MENU = auto()
    IN_SESSION = auto()
    USER_SETTINGS = auto()
    
class StateManager():
    debug_mode: bool = False
    program_version: str = "v1.1.0"

    @staticmethod
    def change_state(user, state: State):
        user.current_state = state
