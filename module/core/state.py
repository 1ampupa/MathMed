from enum import Enum, auto

class State(Enum):
    
    MAIN_MENU = auto()
    IN_SESSION = auto()
    USER_SETTINGS = auto()
    
class StateManager():
    debug_mode = False
    current_state = State.MAIN_MENU

    @classmethod
    def change_state(cls, state: State):
        cls.current_state = state
