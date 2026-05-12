import time
from module.core.utils.state import State, StateManager
from module.core.session.session import Session
from module.core.session.session_telemetry import SessionTelemetry
from module.core.quiz.quiz import Quiz
from module.core.user.user_answer import UserAnswer

class SessionLoop:

    @classmethod
    def loop(cls, session: Session) -> bool:
        if session is None:
            return False
        if not session.active_users:
            return False
        
        # Generate Quiz
        for user in session.active_users:
            while True:
                # Generate question
                quiz = Quiz.generate(user, session.operator)

                # Ask question
                if len(session.active_users) == 1:
                    print(quiz)
                else:
                    print(f"This question goes to {user}!\n{quiz}")

                # Start Quiz Timer
                quiz_start_time = time.perf_counter()

                # Receive User Answer
                answer = input("Answer for world peace: ")

                # Game Quit Handler
                if answer.strip().lower() == 'q':
                    print("You quit the game. Thank you for saving world peace.")
                    session.end_session()
                    return False
                
                quiz_time_taken = time.perf_counter() - quiz_start_time

                # Check User Answer
                try:
                    result = UserAnswer(user, quiz, int(answer))
                except ValueError:
                    print("Invalid input, please answer the question using only numbers.")
                    Quiz.rollback_last_quiz() # Restart the quiz. aka. remove the old one out of the existance :sad:
                    continue

                print(f"{result}! The answer is {result.quiz.answer}.\n")

                # Update difficulty and telemetry
                result.update_difficulty()
                SessionTelemetry.update_telemetry(session, user, result.is_correct, quiz_time_taken)

                # Pop the last index of the five recent performance counter if its length reaches 5
                if len(user.five_recent_answer_results) >= 5:
                    user.five_recent_answer_results.pop(0)

                break

        return True
    