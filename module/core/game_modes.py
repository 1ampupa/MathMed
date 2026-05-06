from enum import Enum

class GameModesIdentifier(Enum):
    ENDLESS = "Endless"
    CHALLENGER_CASUAL = "Challenger: Casual"
    CHALLENGER_REGULAR = "Challenger: Regular"
    CHALLENGER_HARDCORE = "Challenger: Hardcore"
    CUSTOM = "Personalised"

class GameModes:
    def __init__(self, session, mode: GameModesIdentifier):
        self.mode: GameModesIdentifier = mode
        self.session = session
        
        # Defaults (Common)
        self.max_active_users: int = 1
        self.max_questions: int = 20
        self.min_questions_for_report: int = 3
        self.generate_summary_report: bool = True

        # Defaults (Challenge)
        self.max_time_per_question: float = 5.0
        self.max_hearts: int = 3
        self.starting_hearts: int = 3
        self.healable: bool = True

        # Defaults (Difficulty)
        self.adjust_difficulty: bool = True
        self.difficulty_adjust_interval: int  = 5

        if mode != GameModesIdentifier.CUSTOM:
            self._apply_preset(mode)

    def _apply_preset(self, mode: GameModesIdentifier):
        match mode:
            case GameModesIdentifier.ENDLESS:
                self.max_questions = 0
                self.max_time_per_question = 0.0
                self.max_hearts = 0
                self.starting_hearts = 0
            case GameModesIdentifier.CHALLENGER_CASUAL:
                self.max_time_per_question = 0.0
                self.max_hearts = 5
                self.starting_hearts = 5
            case GameModesIdentifier.CHALLENGER_REGULAR:
                self.max_time_per_question = 5.0
                self.max_hearts = 3
                self.starting_hearts = 3
                self.healable = True
            case GameModesIdentifier.CHALLENGER_HARDCORE:
                self.max_time_per_question = 3.0
                self.max_hearts = 3
                self.starting_hearts = 3
                self.healable = False

    def check_arguments(
            self,
            max_active_users: int,
            max_questions: int,
            min_questions_for_report: int,
            generate_summary_report: bool,
            max_hearts: int,
            starting_hearts: int,
            adjust_difficulty: bool,
            difficulty_adjust_interval: int
        ) -> bool:
        if not self.session:
            print("Session do not exist for modifying its settings.")
            return False
        
        if max_active_users <= 0:
            print("Invalid game setting: Needed at least one user in game.")
            return False
            
        # Check session-specific constraints
        if 0 < max_questions < min_questions_for_report and generate_summary_report:
            print(f"Invalid game setting: Needed at least {min_questions_for_report} questions to be able to generate a summary report.")
            return False

        if max_questions != 0: # Non-endless game mode
            if min_questions_for_report > max_questions:
                print("Invalid game setting: Minimum answered questions to generate summary report can't be more than the game max questions.")
                return False

            if starting_hearts < 1 or starting_hearts > max_hearts:
                print("Invalid game setting: Hearts needs to be more than 0 and not less than starting hearts.")
                return False
                
            if adjust_difficulty and difficulty_adjust_interval > max_questions:
                print("Invalid game setting: Difficulty Adjust Interval can't be more than the game max questions.")
                return False

        return True

    def modify_custom(self, **kwargs) -> bool:
        if not self.check_arguments(
                                    kwargs.get('max_active_users', 1),
                                    kwargs.get('max_questions', 20),
                                    kwargs.get('min_questions_for_report', 3),
                                    kwargs.get('generate_summary_report', True),
                                    kwargs.get('max_hearts', 3),
                                    kwargs.get('starting_hearts', 3),
                                    kwargs.get('adjust_difficulty', True),
                                    kwargs.get('difficulty_adjust_interval', 5)
                                    ):
            return False

        self.mode = GameModesIdentifier.CUSTOM
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        return True
    
    def __str__(self) -> str: return self.mode.value
