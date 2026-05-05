from module.core.operators import Operators
from module.core.save_load import SaveLoad
from module.core.difficulty_manager import DifficultyManager
from module.core.state import StateManager, State
from module.core.session import Session

class User:
    users: list[User] = []

    def __init__(self, name: str) -> None:
        # General
        self.name: str = name or "User"
        self.id: str = "_".join(self.name.strip().lower().split())
        self.current_session: Session | None = None
        if StateManager.debug_mode: print(f'Created user: {self.name} with id: {self.id}')

        # Difficulty chart with default value
        self.difficulty_chart: dict = {
            Operators.ADDITION: 10,
            Operators.SUBTRACTION: 10,
            Operators.MULTIPLICATION: 5,
            Operators.DIVISION: 5,
        }

        User.users.append(self)

        # Session Telemetry
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

    @property
    def readable_question_answered(self) -> str:
        if self.question_answered == 1:
            return f'1 question'
        else:
            return f'{self.question_answered} questions'

    # Create user
    @classmethod
    def create(cls) -> User:
        # Get username
        name = input("Enter your name: ")
        # Check for taken username
        for user in cls.users:
            if (name == user.name
                and "_".join(name.strip().lower().split()) == user.id
            ): 
                print("This username is taken. Please try another one.")
                return cls.create()

        return cls(name)

    # Session Telemetry
    def reset_session_telemetry(self) -> None:
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

    # Session
    def connect_session(self, session: Session) -> None:
        # Preventing user joining multiple sessions
        if self.current_session is not None:
            print(f"You are already in the other session ({self.current_session.id}), Disconnect first.")
            return
        
        if StateManager.debug_mode:
            print(f"Connecting {self.name} to the session... (id: {session.id})")
        else:
            print(f"Connecting {self.name} to the session...")
        
        # Session
        self.current_session = session

        # User Telemetry

        StateManager.change_state(State.IN_SESSION)

    def disconnect_session(self, session: Session) -> None:
        if self.current_session is None:
            print(f"You are not in any session.")
            return

        if self.current_session != session:
            print(f"The session to disconnect you from is not match the one you're in.")
            return

        if StateManager.debug_mode:
            print(f"Disconnecting {self.name} from the session (id: {session.id}).")
        else:
            print(f"Disconnecting {self.name} from the session.")
        
        self.current_session = None
        self.reset_session_telemetry()
        StateManager.change_state(State.MAIN_MENU)

    # Difficulty
    def update_difficulty(self, operator: Operators, increase: bool) -> int:
        difficulty = self.difficulty_chart = DifficultyManager.modify_difficulty(
            self.difficulty_chart, operator, increase)
        return difficulty[operator]
