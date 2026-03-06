from module.operator import Operator
from module.difficulty_manager import DifficultyManager

class User:
    
    def __init__(self, name: str) -> None:
        # General
        self.name: str = name or "User"

        # Difficulty chart with default value
        self.difficulty_chart: dict = {
            Operator.ADDITION: 10,
            Operator.SUBTRACTION: 10,
            Operator.MULTIPLICATION: 5,
            Operator.DIVISION: 5,
        }

        # Telemetry
        self.telemetry_accuracy_percentage: float = 0
        self.telemetry_time_per_question: float = 0

    def update_difficulty(self, operator: Operator, increase: bool) -> None:
        self.difficulty_chart = DifficultyManager.modify_difficulty(operator, increase)
        self.difficulty_chart = DifficultyManager.MODIFIER
