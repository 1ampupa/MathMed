from enum import Enum

class GameModesIdentifier(Enum):
    ENDLESS = "Endless" # Base game mode featuring endless gameplay with no challenges
    
    # Challenger Presets
    CHALLENGER_CASUAL = "Challenger: Casual"        # A relaxing gameplay with 5 hearts, healable, no timer
    CHALLENGER_REGULAR = "Challenger: Regular"      # A regular gameplay with 3 hearts, healable, 5 seconds timer per questions
    CHALLENGER_HARDCORE = "Challenger: Hardcore"    # A intense gameplay with 3 hearts, not healable, 3 seconds timer per questions

    CUSTOM = "Personalised" # A full customisable game which you can modify everything in game. Here be dragons!

class GameModes():
    def __init__(self, mode: GameModesIdentifier):
        self.mode = mode
        self.mode_name = mode.value

        # Common variables
        self.max_actives_player: int = 1
        self.max_questions: int = 20 # -1 for Endless

        # Challenge
        self.max_time_per_question: int = 5 # ignored in Endless, and CLG: Casual, 3 in hardcore
        self.max_hearts: int = 3 # ignored in Endless, 5 in CLG: Casual
        self.starting_hearts: int = 3 # ignored in Endless, 5 in CLG: Casual
        self.healable: bool = True # ignored in Endless, false in CLG: Hardcore

        self.modify()

    def modify(self):
        match (self.mode):
            case GameModesIdentifier.ENDLESS:
                self.max_questions = -1
                self.max_time_per_question = -1
            case GameModesIdentifier.CHALLENGER_CASUAL:
                self.max_hearts = 5
                self.starting_hearts = 5
            case GameModesIdentifier.CHALLENGER_REGULAR:
                pass
            case GameModesIdentifier.CHALLENGER_HARDCORE:
                self.max_time_per_question = 3
                self.healable = False
            case GameModesIdentifier.CUSTOM:
                pass
