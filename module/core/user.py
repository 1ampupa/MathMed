from module.core.operators import Operators
from module.core.save_load import SaveLoad
from module.core.difficulty_manager import DifficultyManager
from module.core.state import StateManager
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

    # Difficulty
    def update_difficulty(self, operator: Operators, increase: bool) -> int:
        difficulty = self.difficulty_chart = DifficultyManager.modify_difficulty(
            self.difficulty_chart, operator, increase)
        return difficulty[operator]
