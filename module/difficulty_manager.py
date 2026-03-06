from module.operator import Operator

class DifficultyManager:

    # Constants

    LOWEST_MINIMUM = 0
    LOWEST_MAXIMUM = 5
    HIGHEST_MAXIMUM = 100

    INCREASE_RATE = 1
    DECREASE_RATE = 2

    # Default difficulty
    MODIFIER = {
        Operator.ADDITION: 10,
        Operator.SUBTRACTION: 10,
        Operator.MULTIPLICATION: 5,
        Operator.DIVISION: 5,
    }

    @classmethod
    def set_difficulty_from_user(cls, chart: dict) -> None:
        cls.MODIFIER = chart

    @classmethod
    def modify_difficulty(cls, operator: Operator, increase: bool) -> dict[Operator, int]:
        operator_max = cls.MODIFIER[operator]
        if operator not in cls.MODIFIER: raise ValueError(f"No such difficulty for this operator {operator}")
        operator_max += cls.INCREASE_RATE if increase else - cls.DECREASE_RATE
            
        if operator_max < cls.LOWEST_MAXIMUM: 
            operator_max = cls.LOWEST_MAXIMUM
        elif operator_max > cls.HIGHEST_MAXIMUM:
            operator_max = cls.HIGHEST_MAXIMUM

        cls.MODIFIER[operator] = operator_max

        return cls.MODIFIER
