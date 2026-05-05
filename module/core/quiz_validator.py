from module.core.operators import Operators
from module.core.quiz_modifier import QuizModifier

class QuizValidator:

    @staticmethod
    def validate_quiz(a: int, b: int, operators: Operators) -> bool:
        # Visit 'quiz_modifier.py' for more information and detailed logic
        match (operators):
            case Operators.ADDITION:
                if not QuizModifier.allow_duplicate_addends and a == b: return False
                if not QuizModifier.allow_zero_addend and (a == 0 or b == 0): return False
            case Operators.SUBTRACTION:
                if not QuizModifier.allow_equal_subtraction and a == b: return False
                if not QuizModifier.allow_negative_subtraction and b > a: return False
                if not QuizModifier.allow_zero_subtrahend and b == 0: return False
            case Operators.MULTIPLICATION:
                if not QuizModifier.allow_square_multiplication and a == b: return False
                if not QuizModifier.allow_zero_factor and (a == 0 or b == 0): return False
                if not QuizModifier.allow_one_factor and (a == 1 or b == 1): return False
            case Operators.DIVISION:
                if b == 0: return False
                if not QuizModifier.allow_dividend_equal_divisor and a == b: return False
                if not QuizModifier.allow_zero_dividend and a == 0: return False
                if not QuizModifier.allow_one_divisor and b == 1: return False
            case _:
                return False
        return True # If all conditions are passed; Quiz is able to generate
    