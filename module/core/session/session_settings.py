from enum import Enum

class SessionSettings():

    def __init__(self):
        self.max_active_users: int = 1

        self.endless_mode: bool = True

        self.max_questions_per_player: int = 20 # Per player

        self.timed_mode: bool = False
        self.timed_mode_type: TimedModeType = TimedModeType.PER_QUESTION

        self.health_mode: bool = False
        self.health_mode_max_health: int = 5
        self.health_mode_starting_health: int = 5
        self.health_mode_healable: bool = True
        self.health_mode_shared_health: bool = False

    # Timed Mode

    @property
    def timed_mode_label(self) -> str:
        return self.timed_mode_type.label
    
    @property
    def timed_mode_amount(self) -> int:
        return self.timed_mode_type.amount

class TimedModeType(Enum):
    BANK = ("Bank", 60)
    PER_QUESTION = ("Per question", 5)

    @property
    def label(self) -> str:
        return self.value[0]
    
    @property
    def amount(self) -> int:
        return self.value[1]
