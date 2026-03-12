from module.core.operators import Operators

class DifficultyManager:

    # Constants
    LOWEST_MAXIMUM: int = 5
    HIGHEST_MAXIMUM: dict[Operators, int] = {
        Operators.ADDITION: 100,
        Operators.SUBTRACTION: 100,
        Operators.MULTIPLICATION: 25,
        Operators.DIVISION: 25
    }

    INCREASE_RATE = 1
    DECREASE_RATE = 2

    MINIMUM_ACCURACY_PERCENTAGE_INCREASE = 60 # (answer 3 of 5 questions correctly to increase difficulty)
    
    # Modify user difficulty and return it

    @classmethod
    def modify_difficulty(cls, chart: dict, operator: Operators, increase: bool) -> dict[Operators, int]:
        operator_max = chart[operator]
        operator_max += cls.INCREASE_RATE if increase else - cls.DECREASE_RATE
            
        # Prevent out-of-bound value
        if operator_max < cls.LOWEST_MAXIMUM: 
            operator_max = cls.LOWEST_MAXIMUM
        elif operator_max > cls.HIGHEST_MAXIMUM[operator]:
            operator_max = cls.HIGHEST_MAXIMUM[operator]

        chart[operator] = operator_max

        return chart
