from random import randint, choice

from module.operator import Operator
from module.difficulty_manager import DifficultyManager
from module.quiz_validator import QuizValidator
from module.user import User

class Quiz():
    # Debug Mode
    debug_mode = False

    # Quiz number and Quizzes (Reset on startup and every game session)
    quiz_number: int = 1
    quizzes: list = []
    recent_ten_operands_set: set[tuple[int,int]] = set()

    def __init__(self, a: int, b: int, operator: Operator) -> None:
        self.quiz_number = Quiz.quiz_number
        self._operand_a: int = a
        self._operand_b: int = b
        self._operator: Operator = operator
        self._answer: int = self._operator.apply(self._operand_a, self._operand_b)

        Quiz.quizzes.append(self)
        Quiz.quiz_number += 1

    # Quiz Generator
    @classmethod
    def generate(cls, user: User, operator: Operator) -> Quiz:
        # Pop the first quiz's numbers set when the list reach 10
        if len(cls.recent_ten_operands_set) > 10:
            cls.recent_ten_operands_set.pop()

        min_value = DifficultyManager.LOWEST_MINIMUM
        max_value = user.difficulty_chart[operator]

        if min_value is None or max_value is None:
            raise ValueError(f"Min or Max Value for {operator} cannot be NoneType")
        
        for _ in range(100): # 100 damn attempts so please work ty :D
            a = randint(min_value, max_value)
            b = randint(min_value, max_value)

            # Check for repeating numbers set
            if (a,b) in cls.recent_ten_operands_set:
                continue

            # Generate direct divisible question for division
            if operator is Operator.DIVISION:
                dividend = a * b
                divisor = choice([a,b])
                a = dividend
                b = divisor

            if QuizValidator.validate_quiz(a, b, operator):
                cls.recent_ten_operands_set.add((a,b))
                return cls(a, b, operator)

        raise Exception("No valid quiz generated under this circumstance.")
        
    # Getter Methods

    @property
    def a(self) -> int:
        return self._operand_a

    @property
    def b(self) -> int:
        return self._operand_b

    @property
    def operator(self) -> Operator:
        return self._operator

    @property
    def answer(self) -> int:
        return self._answer

    # Helper Functions

    @staticmethod
    def reset_session() -> None:
        Quiz.quiz_number = 1
        Quiz.quizzes.clear()
    
    def __str__(self) -> str:
        if Quiz.debug_mode:
            return f"{self.quiz_number}. {self._operand_a} {self._operator.value} {self._operand_b} = {self._answer}"
        else:
            return f"{self.quiz_number}. {self._operand_a} {self._operator.value} {self._operand_b} = ?"
