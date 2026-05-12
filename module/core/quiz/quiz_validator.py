from module.core.utils.operators import Operators
from module.core.quiz.quiz_modifier import QuizModifier

class QuizValidator:

    @classmethod
    def fetch(cls, rule: dict, key: str, default):
        return rule.get(key, default)

    @classmethod
    def validate_quiz(cls, modifier: QuizModifier, a: int, b: int, operator: Operators) -> bool:
        # Visit 'quiz_modifier.py' for more information and detailed logic

        # Fetch rules for the specific operator
        rules: dict | None = modifier.rules.get(operator)
        if rules is None: return False

        # Addition
        if not cls.fetch(rules, "allow_duplicate", True) and a == b: return False
        if not cls.fetch(rules, "allow_zero", False) and (a == 0 or b == 0): return False

        # Subtraction
        if not cls.fetch(rules, "allow_equal", False) and a == b: return False
        if not cls.fetch(rules, "allow_negative", False) and b > a: return False
        if not cls.fetch(rules, "allow_zero", False) and b == 0: return False

        # Multiplication
        if not cls.fetch(rules, "allow_square", True) and a == b: return False
        if not cls.fetch(rules, "allow_zero", False) and (a == 0 or b == 0): return False
        if not cls.fetch(rules, "allow_one", False) and (a == 1 or b == 1): return False

        # Division
        if b == 0: return False # nah bro
        if not cls.fetch(rules, "allow_equal", False) and a == b: return False
        if not cls.fetch(rules, "allow_zero", False) and a == 0: return False
        if not cls.fetch(rules, "allow_one", False) and b == 1: return False

        return True # If all conditions are passed; Quiz is able to generate
    