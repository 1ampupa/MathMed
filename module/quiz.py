from random import randint, choice

from module.operator import Operator
from module.quiz_validator import QuizValidator
from module.user import User

class Quiz():
    # Debug Mode (Show answer in the question)
    debug_mode = False

    # Quiz number and Quizzes (Reset on startup and every game session)
    quiz_number: int = 1
    quizzes: list = []
    recent_ten_operands_set: set[tuple[int,int]] = set() # To prevent repeating question

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

        # Fetch max number to generate from user's difficulty chart
        max_value = user.difficulty_chart[operator]

        if max_value is None:
            raise ValueError(f"Max Value for {operator} cannot be NoneType. Please reset this user's difficulty chart.")
        
        for _ in range(100): # 100 damn attempts so please work ty :D
            a = randint(max(1, (max_value//3)), max_value)
            b = randint(max(1, (max_value//3)), max_value)

            # Check for repeating numbers set
            if (a,b) in cls.recent_ten_operands_set:
                continue

            # Generate direct divisible question for division
            if operator is Operator.DIVISION:
                dividend = a * b
                divisor = choice([a,b])
                a = dividend
                b = divisor

            # Validate quiz
            if QuizValidator.validate_quiz(a, b, operator):
                cls.recent_ten_operands_set.add((a,b))
                return cls(a, b, operator)

        # End session if there's no quiz able to generate
        if user.current_session:
            user.current_session.disconnect_user()

        raise ValueError("No valid quiz generated under this condition. Please change your quiz settings or revert to default settings.")
        
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
