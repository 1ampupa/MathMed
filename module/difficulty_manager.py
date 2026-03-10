from module.operator import Operator

class DifficultyManager:

    # Constants

    LOWEST_MAXIMUM: int = 5
    HIGHEST_MAXIMUM: dict[Operator, int] = {
        Operator.ADDITION: 100,
        Operator.SUBTRACTION: 100,
        Operator.MULTIPLICATION: 25,
        Operator.DIVISION: 25
    }

    INCREASE_RATE = 1
    DECREASE_RATE = 2

    @classmethod
    def modify_difficulty(cls, chart: dict, operator: Operator, increase: bool) -> dict[Operator, int]:
        operator_max = chart[operator]
        operator_max += cls.INCREASE_RATE if increase else - cls.DECREASE_RATE
            
        if operator_max < cls.LOWEST_MAXIMUM: 
            operator_max = cls.LOWEST_MAXIMUM
        elif operator_max > cls.HIGHEST_MAXIMUM[operator]:
            operator_max = cls.HIGHEST_MAXIMUM[operator]

        chart[operator] = operator_max

        return chart
