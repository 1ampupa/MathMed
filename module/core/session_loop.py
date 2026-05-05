import time
from module.core.state import State, StateManager
from module.core.session import Session
from module.core.session_telemetry import SessionTelemetry
from module.core.quiz import Quiz
from module.core.user_answer import UserAnswer

class SessionLoop:

    @classmethod
    def loop(cls, session: Session) -> bool:
        if session is None:
            return False
        if session.active_user is None:
            return False
        # Generate Quiz
        quiz = Quiz.generate(session.active_user, session.operator)
        print(quiz)

        # Start Quiz Timer
        quiz_start_time = time.perf_counter()

        # Receive User Answer
        answer = input("Answer for world peace: ")

        # Game Quit Handler (temporary)
        if answer.strip().lower() == 'q':
            print("You quit the game. Thank you for saving world peace.")
            session.end_session()
            StateManager.change_state(State.MAIN_MENU)
            return False
        
        quiz_time_taken = time.perf_counter() - quiz_start_time

        # Check User Answer
        try:
            result = UserAnswer(session.active_user, quiz, int(answer))
        except ValueError:
            print("Invalid input, please answer the question using only numbers.")
            Quiz.rollback_last_quiz() # Restart the quiz. aka. remove the old one out of the existance :sad:
            return False

        print(f"{result}! The answer is {result.quiz.answer}.\n")

        # Update difficulty and telemetry
        result.update_difficulty()
        SessionTelemetry.update_telemetry(session ,result.is_correct, quiz_time_taken)

        # Pop the last index of the five recent performance counter if its length reaches 5
        if len(session.five_recent_answer_results) >= 5:
            session.five_recent_answer_results.pop(0)

        return True
    