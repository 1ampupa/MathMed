from module.core.difficulty_manager import DifficultyManager
from module.core.user import User
from module.core.quiz import Quiz

class UserAnswer:
    def __init__(self, user: User, quiz: Quiz, user_answer: int) -> None:
        self.user = user
        self.quiz = quiz
        self.answer = user_answer

    @property # Return a boolean result
    def is_correct(self) -> bool: return True if self.answer == self.quiz.answer else False
    
    @property # Return a readable result
    def result(self) -> str: return "Correct" if self.is_correct else "Incorrect"
       
    # Check condition from session wheather to increase or decrase the difficulty
    def update_difficulty(self) -> None:
        if self.user.current_session is not None:
            # Update difficulty every 5 quiz based on overall accuracy and recent performance
            if self.quiz.quiz_number % 5 == 0:
                if (
                    self.user.current_session.accuracy_percentage >= 
                    DifficultyManager.MINIMUM_ACCURACY_PERCENTAGE_INCREASE
                and (sum(self.user.current_session.five_recent_answer_results)) * 20 >= # * 20 to make it percentage
                    DifficultyManager.MINIMUM_ACCURACY_PERCENTAGE_INCREASE
                ):
                    difficulty = self.user.update_difficulty(self.quiz.operator, True)
                    print(f"Quiz difficulty is now increased. Now {difficulty}/{DifficultyManager.HIGHEST_MAXIMUM[self.quiz.operator]}")
                else:
                    difficulty = self.user.update_difficulty(self.quiz.operator, False)
                    print(f"Quiz difficulty is now decreased. Now {difficulty}/{DifficultyManager.HIGHEST_MAXIMUM[self.quiz.operator]}")
    
    def __str__(self) -> str:
        return self.result
