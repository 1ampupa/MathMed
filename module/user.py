from module.operator import Operator
from module.difficulty_manager import DifficultyManager
from module.session import Session

class User:
    def __init__(self, name: str) -> None:
        # General
        self.name: str = name or "User"
        self.current_session: Session | None = None

        # Difficulty chart with default value
        self.difficulty_chart: dict = {
            Operator.ADDITION: 10,
            Operator.SUBTRACTION: 10,
            Operator.MULTIPLICATION: 5,
            Operator.DIVISION: 5,
        }

    # Difficulty
    def update_difficulty(self, operator: Operator, increase: bool) -> int:
        difficulty = self.difficulty_chart = DifficultyManager.modify_difficulty(
            self.difficulty_chart, operator, increase)
        return difficulty[operator]
