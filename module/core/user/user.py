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

        # State
        self.current_state: State = State.IDLE

        User.users.append(self)
        if StateManager.debug_mode: print(f'Created user: {self.name} with id: {self.id}')

    # Create user
    @classmethod
    def create(cls, name: str = "User") -> User:
        # Get username
        while True:
            name = name or input("Enter your name: ")

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
