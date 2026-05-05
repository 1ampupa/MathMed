from module.core.state import State, StateManager
from module.core.session import Session
from module.core.user import User

class SessionTelemetry():
    
    @staticmethod
    def update_telemetry(session: Session, user: User, is_correct: bool, time_elapsed: float) -> None:
        if not session or not user:
            return
        
        # Update Statstic
        session.all_question_answered += 1
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
            user.points -= 1 # Base point for incorrect answer
            user.incorrect_answer += 1

            if user.correct_streak >= 5:
                # Annouce end of streak if user has 5+ streak
                print(f"{user.correct_streak} streaks has ended!\n")

            user.correct_streak = 0
        
        # Calculate Accuracy
        user.accuracy_percentage = round((user.correct_answer / user.question_answered) * 100)

        # Reset point if it went negative
        if user.points < 0: user.points = 0

        # Pop the last index of the five recent performance counter if its length reaches 5
        if len(user.five_recent_answer_results) >= 5:
            user.five_recent_answer_results.pop(0)

    @staticmethod
    def summarise_telemetry(session: Session, user: User) -> None:
        if session is None:
            print("No session to generate a summary report.")
            return
        if session.active_users is not None:
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
                    f"Longest streak: {user.max_correct_streak}\n",
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
                    f"Question asked by the game: {session.all_question_answered}",
                    f"Accuracy: {user.accuracy_percentage}% ({user.correct_answer}/{user.question_answered})\n",
                    f"Longest streak: {user.max_correct_streak}\n",
                    f"Avg. Time/Question: {user.average_time_per_question:.2f} seconds\n",
                    f"{"="*50}"
                )
        else:
            print("Failed to generate a session summary report without any active user.")
