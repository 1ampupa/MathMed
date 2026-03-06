from module.user import User
from module.quiz import Quiz

class UserAnswer():
    def __init__(self, user: User, quiz: Quiz, user_answer: int) -> None:
        self.user = user
        self.quiz = quiz
        self.answer = user_answer

    @property
    def result(self) -> str:
        if self.answer == self.quiz.answer:
            self.user.update_difficulty(self.quiz.operator, True)
            return "Correct!"
        else:
            self.user.update_difficulty(self.quiz.operator, False)
            return "Incorrect!"

    def __str__(self) -> str:
        return self.result
