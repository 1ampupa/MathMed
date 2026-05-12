from enum import Enum, auto

class State(Enum):
    
    IDLE = auto()
    IN_SESSION = auto()
    USER_SETTINGS = auto()
    
class StateManager():
    debug_mode: bool = False
    if debug_mode:
        program_version: str = "v1.1.0 Development Build"
    else:
        program_version: str = "v1.1.0"

    @classmethod
    def change_state(cls, state: State) -> None:
        cls.current_state = state
