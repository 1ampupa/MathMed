from enum import Enum

from module.core.session.session_settings import SessionSettings, TimedModeType, HealthModeType
from module.core.utils.exceptions import UnknownSessionPresetIdentifier

class SessionPresetIdentifier(Enum):
    # Default preset
    STANDARD = "Standard" # A default gameplay with no timer or hearts.
    ENDLESS_DEFAULT = "Endless" # Features no limit and no timer and hearts.
    SWIFT_ROUND = "Swift Round" # Features a 3 seconds per question with 3 hearts, has bonus heart for streak.
    PERFECTION = "Perfection" # No mistakes are accepted here.
    
    CUSTOM = "Personalised" # Your freestyle gameplay.

    # Experimental preset (Requrired Debug mode)
    ONBOARDING = "Onboarding" # Play for the first time
    ENDLESS_CHALLENGER = "Endless Challenger" # Similar to endless mode but features a 5 seconds timer and 3 hearts
    MASTERS = "Masters" # Built upon Perfection mode but features a 3 seconds timer
    MARATHON_FUN_RUN = "Marathon Fun Run" # Answer as many as you can in 60 seconds, mistake doesn't deduct time, has bonus time for streak.
    MARATHON_FINISHER = "Marathon Finisher" # Answer as many as you can in 120 seconds, mistake deducts time, has bonus time for streak.

class SessionPreset(SessionSettings):
    def __init__(self, preset: SessionPresetIdentifier) -> None:
        super().__init__()

        match (preset):
            case SessionPresetIdentifier.STANDARD:
                self.endless_mode = False
                self.timed_mode_enabled = False
                self.health_mode_enabled = False
            case SessionPresetIdentifier.ENDLESS_DEFAULT:
                self.endless_mode = True
                self.timed_mode_enabled = False
                self.health_mode_enabled = False
            case SessionPresetIdentifier.ENDLESS_CHALLENGER:
                self.endless_mode = True

                self.timed_mode_enabled = True
                self.timed_mode_type = TimedModeType.PER_QUESTION
                self.time_duration = 5
                self.mistake_deduct_time = False

                self.health_mode_enabled = True
                self.health_mode_type = HealthModeType.INDIVIDUAL
                self.max_health = 3
                self.starting_health = 3
                self.healable = True
            case SessionPresetIdentifier.SWIFT_ROUND:
                self.endless_mode = False

                self.timed_mode_enabled = True
                self.timed_mode_type = TimedModeType.PER_QUESTION
                self.time_duration = 3
                self.mistake_deduct_time = False

                self.health_mode_enabled = True
                self.health_mode_type = HealthModeType.INDIVIDUAL
                self.max_health = 3
                self.starting_health = 3
                self.healable = True
            case SessionPresetIdentifier.PERFECTION:
                self.endless_mode = False

                self.timed_mode_enabled = False

                self.health_mode_enabled = True
                self.health_mode_type = HealthModeType.INDIVIDUAL
                self.max_health = 1
                self.starting_health = 1
                self.healable = False
            case SessionPresetIdentifier.MASTERS:
                self.endless_mode = False
                
                self.timed_mode_enabled = True
                self.timed_mode_type = TimedModeType.PER_QUESTION
                self.time_duration = 3
                self.mistake_deduct_time = False

                self.health_mode_enabled = True
                self.health_mode_type = HealthModeType.INDIVIDUAL
                self.max_health = 1
                self.starting_health = 1
                self.healable = False
            case SessionPresetIdentifier.MARATHON_FUN_RUN:
                self.endless_mode = False
                
                self.timed_mode_enabled = True
                self.timed_mode_type = TimedModeType.BANK
                self.time_duration = 60
                self.mistake_deduct_time = False

                self.health_mode_enabled = False
            case SessionPresetIdentifier.MARATHON_FINISHER:
                self.endless_mode = False
                
                self.timed_mode_enabled = True
                self.timed_mode_type = TimedModeType.BANK
                self.time_duration = 120
                self.mistake_deduct_time = True

                self.health_mode_enabled = False
            case SessionPresetIdentifier.ONBOARDING:
                self.max_questions_per_player = 10

                self.endless_mode = False
                self.timed_mode_enabled = False
                self.health_mode_enabled = False

            case _: raise UnknownSessionPresetIdentifier()
