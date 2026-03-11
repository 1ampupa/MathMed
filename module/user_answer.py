from module.operator import Operator
from module.user import User
from module.quiz import Quiz

class UserAnswer:
    def __init__(self, user: User, quiz: Quiz, user_answer: int) -> None:
        self.user = user
        self.quiz = quiz
        self.answer = user_answer

    @property
    def result(self) -> str:
        return "Correct" if self.answer == self.quiz.answer else "Incorrect"
    
    @property
    def is_correct(self) -> bool:
        return True if self.answer == self.quiz.answer else False
        
    def update_difficulty(self) -> bool:
        if self.quiz.operator == Operator.ADDITION or self.quiz.operator == Operator.SUBTRACTION:
            if self.quiz.quiz_number % 3 == 0:
                increase = True if self.answer == self.quiz.answer else False
                self.user.update_difficulty(self.quiz.operator, increase)
                return True
        elif self.quiz.operator == Operator.MULTIPLICATION or self.quiz.operator == Operator.DIVISION:
            if self.quiz.quiz_number % 5 == 0:
                increase = True if self.answer == self.quiz.answer else False
                self.user.update_difficulty(self.quiz.operator, increase)
                return True
        return False

    def __str__(self) -> str:
        return self.result
