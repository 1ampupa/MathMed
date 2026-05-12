from module.core.utils.operators import Operators
from module.core.utils.difficulty_manager import DifficultyManager
from module.core.utils.state import StateManager, State

class User:
    users: list[User] = []

    def __init__(self, name: str) -> None:
        # General
        self.name: str = name or "User"
        self.id: str = "_".join(self.name.strip().lower().split())

        # Difficulty chart with default value
        self.difficulty_chart: dict = {
            Operators.ADDITION: 10,
            Operators.SUBTRACTION: 10,
            Operators.MULTIPLICATION: 5,
            Operators.DIVISION: 5,
        }

        # Session
        self.current_session = None

        # Session telemetry
        self.question_answered: int = 0
        self.points: int = 0
        self.correct_answer: int = 0
        self.incorrect_answer: int = 0
        self.correct_streak: int = 0
        self.max_correct_streak: int = 0
        self.accuracy_percentage: int = 0
        self.time_elapsed: float = 0
        self.average_time_per_question: float = 0
        self.five_recent_answer_results: list = []

        # State
        self.current_state: State = State.IDLE

        User.users.append(self)
        if StateManager.debug_mode: print(f'Created user: {self.name} with id: {self.id}')

    # Create user
    @classmethod
    def create(cls, name: str = "User", cli_mode: bool = False) -> User:
        if StateManager.debug_mode: return cls("Test User")
        # Get username
        while True:
            if cli_mode:
                name = input("Enter your name: ")

            # Check for taken username
            is_taken = any(
                 name == user.name or "_".join(name.strip().lower().split()) == user.id
                 for user in cls.users
            )

            if is_taken:
                print("This username is taken. Please try another one.")
                name = "" # Reset the input
                continue

            return cls(name)

    # Difficulty
    def update_difficulty(self, operator: Operators, increase: bool) -> int:
        difficulty = self.difficulty_chart = DifficultyManager.modify_difficulty(
            self.difficulty_chart, operator, increase)
        return difficulty[operator]

    # Session
    def connect_session(self, session) -> None:
        if not session: return
        self.current_session = session
        self.current_state = State.IN_SESSION

    def disconnect_session(self) -> None:
        if self.current_session is None: return
        self.current_session = None
        self.current_state = State.IDLE
        self.clean_session_telemetry()

    def clean_session_telemetry(self) -> None:
        self.question_answered = 0
        self.points = 0
        self.correct_answer = 0
        self.incorrect_answer = 0
        self.correct_streak = 0
        self.max_correct_streak = 0
        self.accuracy_percentage = 0
        self.time_elapsed = 0
        self.average_time_per_question = 0
        self.five_recent_answer_results = []

    @property
    def readable_question_answered(self) -> str:
        if self.question_answered == 1:
            return f'1 question'
        else:
            return f'{self.question_answered} questions'

