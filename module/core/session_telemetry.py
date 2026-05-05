from module.core.state import State, StateManager
from module.core.session import Session

class SessionTelemetry():
    
    @staticmethod
    def update_telemetry(session: Session, is_correct: bool, time_elapsed: float) -> None:
        if not session:
            return
        # Update Statstic
        session.question_answered += 1
        session.time_elapsed += time_elapsed

        if is_correct:
            session.points += 1 # Base point for correct answer
            session.correct_answer += 1
            session.correct_streak += 1
            session.five_recent_answer_results.append(is_correct)

            if session.correct_streak % 5 == 0:
                # Annouce streak for every 5 correct answers
                print(f"Correct {session.correct_streak} times in a row, +1 Point!\n")
                # Bonus +1 Point for every 5 correct answers
                session.points += 1

            if session.correct_streak > session.max_correct_streak: # Record max streak
                session.max_correct_streak = session.correct_streak
        else:
            session.points -= 1 # Base point for incorrect answer
            session.incorrect_answer += 1

            if session.correct_streak >= 5:
                # Annouce end of streak if user has 5+ streak
                print(f"{session.correct_streak} streaks has ended!\n")

            session.correct_streak = 0
        
        # Calculate Accuracy
        session.accuracy_percentage = round((session.correct_answer / session.question_answered) * 100)

        # Reset point if it went negative
        if session.points < 0: session.points = 0

    @staticmethod
    def summarise_telemetry(session: Session) -> None:
        if session is None:
            print("No session to generate a summary report.")
            return
        if session.active_user is not None:
            if not StateManager.debug_mode: # General result
                print(
                    f"{"="*50}\n"
                    f"Summary Report\n",
                    f"User: {session.active_user.name}\n",
                    f"You earned a total of {session.points} points!\n",
                    f"Game mode: {session.readable_operator} ({session.operator.name})\n",
                    f"Time elapsed: {session.time_elapsed:.1f} seconds\n\n",
                    f"Question answered: {session.readable_question_answered}\n",
                    f"Accuracy: {session.accuracy_percentage}% ({session.correct_answer}/{session.question_answered})\n",
                    f"Longest streak: {session.max_correct_streak}\n",
                    f"Avg. Time/Question: {session.average_time_per_question:.1f} seconds\n",
                    f"{"="*50}"
                )
            else: # Technical result
                print(
                    f"{"="*50}\n"
                    f"Summary Report for session {session.id}.\n",
                    f"User: {session.active_user.name} (user id: {session.active_user.id})\n",
                    f"Earned {session.points} points!\n",
                    f"Game mode: {session.readable_operator} ({session.operator})\n",
                    f"Time elapsed: {session.time_elapsed:.2f} seconds\n\n",
                    f"Question answered: {session.readable_question_answered}\n",
                    f"Accuracy: {session.accuracy_percentage}% ({session.correct_answer}/{session.question_answered})\n",
                    f"Longest streak: {session.max_correct_streak}\n",
                    f"Avg. Time/Question: {session.average_time_per_question:.2f} seconds\n",
                    f"{"="*50}"
                )
        else:
            print("Failed to generate a session summary report without any active user.")
