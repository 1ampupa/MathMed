from random import randint, choice

from module.core.utils.operators import Operators
from module.core.utils.exceptions import QuizGenerationExceededLimit
from module.core.utils.state import StateManager
from module.core.quiz.quiz_validator import QuizValidator
from module.core.user.user import User

class Quiz():

    # Quiz number and Quizzes (Reset on startup and every game session)
    quiz_number: int = 1
    quizzes: list = []
    recent_ten_operands_set: list[tuple[int,int]] = []
    max_generation_attempt: int = 100

    def __init__(self, a: int, b: int, operator: Operators) -> None:
        self.quiz_number = Quiz.quiz_number
        self._operand_a: int = a
        self._operand_b: int = b
        self._operator: Operators = operator
        self._answer: int = self._operator.apply(self._operand_a, self._operand_b)

        Quiz.quizzes.append(self)
        Quiz.quiz_number += 1

    # Quiz Generator

    @classmethod
    def generate(cls, user: User, operator: Operators) -> Quiz:
        # Pop the first quiz's numbers set when the list reach 10
        if len(cls.recent_ten_operands_set) > 10:
            cls.recent_ten_operands_set.pop(0)

        # Fetch the maximum number to generate from user's difficulty chart
        max_value: int = user.difficulty_chart[operator]

        if max_value is None:
            raise ValueError(f"Max Value for {operator} cannot be NoneType. Please reset this user's difficulty chart.")
        
        # Set the minimum value from the 1/3 of maximum number else 1 as a fail-safe
        min_value: int = max(1, max_value//3)

        for _ in range(cls.max_generation_attempt): # 100 damn attempts so please work ty :D
            a = randint(min_value, max_value)
            b = randint(min_value, max_value)

            # Check for repeating numbers in the list
            if (
                (a,b) in cls.recent_ten_operands_set
                or (b,a) in cls.recent_ten_operands_set
            ):
                continue

            # Generate direct divisible question for division
            if operator is Operators.DIVISION:
                dividend = a * b
                divisor = choice([a,b])
                a = dividend
                b = divisor

            # Validate quiz
            if QuizValidator.validate_quiz(a, b, operator):
                cls.recent_ten_operands_set.append((a,b))
                return cls(a, b, operator)

        raise QuizGenerationExceededLimit()
        
    # Getter Methods

    @property
    def a(self) -> int:
        return self._operand_a

    @property
    def b(self) -> int:
        return self._operand_b

    @property
    def operator(self) -> Operators:
        return self._operator

    @property
    def answer(self) -> int:
        return self._answer

    # Helper Functions

    @classmethod
    def reset_session(cls) -> None:
        cls.quiz_number = 1
        cls.quizzes.clear()
    
    @staticmethod
    def rollback_last_quiz() -> None:
        if Quiz.quizzes:
            Quiz.quizzes.pop()
            Quiz.quiz_number = len(Quiz.quizzes) + 1

    def __str__(self) -> str:
        if StateManager.debug_mode:
            return f"{self.quiz_number}. {self._operand_a} {self._operator.value} {self._operand_b} = {self._answer}"
        else:
            return f"{self.quiz_number}. {self._operand_a} {self._operator.value} {self._operand_b} = ?"
