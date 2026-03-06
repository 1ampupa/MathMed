from module.operator import Operator

class DifficultyManager:
    BASE = {
        Operator.ADDITION: (0, 10),
        Operator.SUBTRACTION: (0, 10),
        Operator.MULTIPLICATION: (0, 10),
        Operator.DIVISION: (0, 10),
    }