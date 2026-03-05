from module.operator import Operator
from module.difficulty_manager import DifficultyManager
from random import randint

class Quiz():
    # Debug Mode
    debug_mode = False

    # Modifier
    allow_negative_subtraction_answer = False

    # Quiz number and Quizzes (Reset on startup and every game session)
    quiz_number: int = 1
    quizzes: list = []

    def __init__(self, a: int, b: int, operator: Operator) -> None:
        self.quiz_number = Quiz.quiz_number
        self._a: int = a
        self._b: int = b
        self._operator: Operator = operator
        self._answer: int = self._operator.apply(self._a, self._b)

        Quiz.quizzes.append(self)
        Quiz.quiz_number += 1

    # Quiz Generator
    @classmethod
    def generate(cls, operator: Operator) -> Quiz:
        min_value, max_value = DifficultyManager.BASE[operator]
        
        # TODO Difficulty Modifier
        
        if operator is Operator.SUBTRACTION and not cls.allow_negative_subtraction_answer:
            a = randint(min_value, max_value)
            b = randint(min_value, a)   
        elif operator is Operator.DIVISION:
            b = randint(min_value, max_value)
            answer = randint(min_value, max_value)
            a = b * answer
        else:
            a = randint(min_value, max_value)
            b = randint(min_value, max_value)

        return cls(a, b, operator)

    # Getter Methods

    @property
    def a(self) -> int:
        return self._a

    @property
    def b(self) -> int:
        return self._b

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
            return f"{self.quiz_number}. {self._a} {self._operator.value} {self._b} = {self._answer}"
        else:
            return f"{self.quiz_number}. {self._a} {self._operator.value} {self._b} = ?"
