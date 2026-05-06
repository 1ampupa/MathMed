import time
from module.core.game_modes import GameModes
from module.core.session import Session
from module.core.session_telemetry import SessionTelemetry
from module.core.quiz import Quiz
from module.core.user_answer import UserAnswer

class SessionLoop:

    @classmethod
    def loop(cls, session: Session) -> bool:
        if session is None:
            return False
        if session.active_users is None:
            return False
        
        # Loop through active users
        for user in session.active_users:
            while True:
                if session.game_mode.max_questions != 0:
                    if session.all_question_answered >= session.game_mode.max_questions:
                        print("World peace secured! Thank you for saving world peace")
                        session.end_session()
                        return False

                # Generate Quiz
                quiz = Quiz.generate(user, session.operator)
                if len(session.active_users) > 1:
                    print(f"This question goes to {user.name}!\n{quiz}")
                else:
                    print(quiz)

                # Start Quiz Timer
                quiz_start_time = time.perf_counter()

                # Receive User Answer
                answer = input("Answer for world peace: ")

                # Game Quit Handler (temporary)
                if answer.strip().lower() == 'q':
                    print("You quit the game. Thank you for saving world peace.")
                    if len(session.active_users) == 1:
                        session.end_session()
                        return False
                    else:
                        session.disconnect_user(user)
                        return True
                
                quiz_time_taken = time.perf_counter() - quiz_start_time

                # Check User Answer
                try:
                    result = UserAnswer(user, quiz, int(answer))
                    print(f"{result}! The answer is {result.quiz.answer}.\n")

                    # Update difficulty and telemetry
                    SessionTelemetry.update_telemetry(session, user, result.is_correct, quiz_time_taken)
                    if session.game_mode.adjust_difficulty: result.update_difficulty()
                    break # Continue to next user
                except ValueError:
                    print("Invalid input, please answer the question using only numbers.")
                    Quiz.rollback_last_quiz() # Restart the quiz. aka. remove the old one out of the existance :skull:

        return True
    