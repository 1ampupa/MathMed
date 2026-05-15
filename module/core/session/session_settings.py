from enum import Enum

class TimedModeType(Enum):
    BANK = "Bank"
    PER_QUESTION = "Per question"

class HealthModeType(Enum):
    INDIVIDUAL = "Individual"
    SHARED = "Shared"

class SessionSettings():

    def __init__(self):
        # Default Settings

        self.max_active_users: int = 1

        self.endless_mode: bool = False

        self.max_questions_per_player: int = 20 # Per player

        self.timed_mode_enabled: bool = False
        self.timed_mode_type: TimedModeType = TimedModeType.PER_QUESTION
        self.time_duration: int = 5 # In seconds, change depends on TimedModeType
        self.mistake_deduct_time: bool = False

        self.health_mode_enabled: bool = False
        self.health_mode_type: HealthModeType = HealthModeType.INDIVIDUAL
        self.max_health: int = 3
        self.starting_health: int = self.max_health
        self.healable: bool = True
