from module.core.utils.state import State, StateManager
from module.core.session.session import Session
from module.core.user.user import User

class SessionTelemetry():
    
    @staticmethod
    def update_telemetry(session: Session, user: User, is_correct: bool, time_elapsed: float) -> None:
        if not session:
            return
        # Update Statstic
        session.question_asked += 1

        user.question_answered += 1
        user.time_elapsed += time_elapsed

        if is_correct:
            user.points += 1 # Base point for correct answer
            user.correct_answer += 1
            user.correct_streak += 1
            user.five_recent_answer_results.append(is_correct)

            if user.correct_streak % 5 == 0:
                # Annouce streak for every 5 correct answers
                print(f"Correct {user.correct_streak} times in a row, +1 Point!\n")
                # Bonus +1 Point for every 5 correct answers
                user.points += 1

            if user.correct_streak > user.max_correct_streak: # Record max streak
                user.max_correct_streak = user.correct_streak
        else:
            user.incorrect_answer += 1

            if user.correct_streak >= 5:
                # Annouce end of streak if user has 5+ streak
                print(f"Streak of {user.correct_streak} has ended!\n")

            user.correct_streak = 0
        
        # Calculate Accuracy
        user.accuracy_percentage = round((user.correct_answer / user.question_answered) * 100)

        # Reset point if it went negative
        if user.points < 0: user.points = 0

    @staticmethod
    def summarise_telemetry(session: Session, user) -> None:
        if session is None:
            print("No session to generate a summary report.")
            return
        if user is not None:
            if not StateManager.debug_mode: # General result
                print(
                    f"{"="*50}\n"
                    f"Summary Report\n",
                    f"User: {user.name}\n",
                    f"You earned a total of {user.points} points!\n",
                    f"Game mode: {session.readable_operator} ({session.operator.name})\n",
                    f"Time elapsed: {user.time_elapsed:.1f} seconds\n\n",
                    f"Question answered: {user.readable_question_answered}\n",
                    f"Accuracy: {user.accuracy_percentage}% ({user.correct_answer}/{user.question_answered})\n",
                    f"Longest streak: {user.max_correct_streak} questions\n",
                    f"Avg. Time/Question: {user.average_time_per_question:.1f} seconds\n",
                    f"{"="*50}"
                )
            else: # Technical result
                print(
                    f"{"="*50}\n"
                    f"Summary Report for session {session.id}.\n",
                    f"User: {user.name} (user id: {user.id})\n",
                    f"Earned {user.points} points!\n",
                    f"Game mode: {session.readable_operator} ({session.operator})\n",
                    f"Time elapsed: {user.time_elapsed:.2f} seconds\n\n",
                    f"Question answered: {user.readable_question_answered}\n",
                    f"All questions asked by the game: {session.question_asked} questions\n",
                    f"Accuracy: {user.accuracy_percentage}% ({user.correct_answer}/{user.question_answered})\n",
                    f"Longest streak: {user.max_correct_streak} questions\n",
                    f"Avg. Time/Question: {user.average_time_per_question:.2f} seconds\n",
                    f"{"="*50}"
                )
        else:
            print("Failed to generate a session summary report without any active user.")
