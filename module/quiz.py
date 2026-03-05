from module.operator import Operator

class Quiz():
    # Debug Mode
    debug_mode = False
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
    
    def __str__(self) -> str:
        if Quiz.debug_mode:
            return f"{self.quiz_number}. {self._a} {self._operator.value} {self._b} = {self._answer}"
        else:
            return f"{self.quiz_number}. {self._a} {self._operator.value} {self._b} = ?"

    # Helper Functions

    @staticmethod
    def reset_session() -> None:
        Quiz.quiz_number = 1
        Quiz.quizzes.clear()
    
