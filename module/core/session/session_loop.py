import time
from module.core.utils.state import State, StateManager
from module.core.session.session import Session
from module.core.session.session_telemetry import SessionTelemetry
from module.core.quiz.quiz import Quiz
from module.core.user.user_answer import UserAnswer

class SessionLoop:

    quit_attempted: bool = False

    @classmethod
    def is_answered_every_question(cls, session: Session) -> bool:
        if (
            not session.preset.endless_mode
            and session.question_asked >= session.preset.max_questions_per_player * session.preset.max_active_users
        ):
            return True
        else: return False

    @classmethod
    def loop(cls, session: Session) -> bool:
        if session is None or not session.active_users:
            return False
        
        # Check if everyone has completed all of their available question
        if cls.is_answered_every_question(session):
            print("GAME! Thank you for playing.")
            session.end_session()
            return False

        # Generate Quiz
        for user in session.active_users:
            # Generate question
            quiz = Quiz.generate(session, user, session.operator)

            # Start Quiz Timer
            quiz_start_time = time.perf_counter()

            while True:
                # Ask question
                if not cls.quit_attempted:
                    if len(session.active_users) == 1:
                        print(quiz)
                    else:
                        print(f"This question goes to {user}!\n{quiz}")

                # Receive User Answer
                answer = input("Answer for world peace: ")

                # Game Quit Handler
                if answer.strip().lower() == 'q':
                    if not cls.quit_attempted:
                        if not cls.is_answered_every_question(session) and user.question_answered >= session.minimum_answer_for_report:
                            cls.quit_attempted = True
                            print("The game haven't finished yet. Are you sure you want to quit?\nType 'q' again to confirm.")
                            continue
                        elif not cls.is_answered_every_question(session) and user.question_answered < session.minimum_answer_for_report:
                            cls.quit_attempted = True
                            print("The game haven't finished yet. Are you sure you want to abandon the game?\nYou will not receive any summary report!\nType 'q' again to confirm.")
                            continue
                    else:
                        print("You quit the game. Thank you for saving world peace.")
                        session.end_session()
                        return False
                
                quiz_time_taken = time.perf_counter() - quiz_start_time

                # Reset Quit attempt
                cls.quit_attempted = False

                # Check User Answer
                try:
                    result = UserAnswer(user, quiz, int(answer))

                    print(f"{result}! The answer is {result.quiz.answer}.\n")

                    # Update difficulty and telemetry
                    result.update_difficulty()
                    SessionTelemetry.update_telemetry(session, user, result.is_correct, quiz_time_taken)

                    break
                except ValueError:
                    if not cls.quit_attempted:
                        print("Invalid input, please answer the question using only numbers.\n")
                    continue # restart the quiz (timer still continue)
        return True
    