from module.operator import Operator
from module.quiz_modifier import QuizModifier

class QuizValidator:
    @staticmethod
    def validate_quiz(a: int, b: int, operator: Operator) -> bool:
        match (operator):
            case Operator.ADDITION:
                if not QuizModifier.allow_duplicate_addends and a == b: return False
                if not QuizModifier.allow_zero_addend and (a == 0 or b == 0): return False
            case Operator.SUBTRACTION:
                if not QuizModifier.allow_equal_subtraction and a == b: return False
                if not QuizModifier.allow_negative_subtraction and b > a: return False
                if not QuizModifier.allow_zero_subtrahend and b == 0: return False
            case Operator.MULTIPLICATION:
                if not QuizModifier.allow_square_multiplication and a == b: return False
                if not QuizModifier.allow_zero_factor and (a == 0 or b == 0): return False
                if not QuizModifier.allow_one_factor and (a == 1 or b == 1): return False
            case Operator.DIVISION:
                if b == 0: return False
                if not QuizModifier.allow_dividend_equal_divisor and a == b: return False
                if not QuizModifier.allow_zero_dividend and a == 0: return False
                if not QuizModifier.allow_one_divisor and b == 1: return False
            case _:
                return False
        return True
    