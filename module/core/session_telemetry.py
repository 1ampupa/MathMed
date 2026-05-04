from module.core.state import State, StateManager
from module.core.session import Session

class SessionTelemetry():

    current_session: Session | None = None

    @classmethod
    def update_telemetry(cls, is_correct: bool, time_elapsed: float) -> None:
        if not cls.current_session:
            return
        # Update Statstic
        cls.current_session.question_answered += 1
        cls.current_session.time_elasped += time_elapsed

        if is_correct:
            cls.current_session.points += 1 # Base point for correct answer
            cls.current_session.correct_answer += 1
            cls.current_session.correct_streak += 1
            cls.current_session.five_recent_answer_results.append(is_correct)

            if cls.current_session.correct_streak % 3 == 0:
                # Annouce streak every 3 correct answers
                print(f"Correct {cls.current_session.correct_streak} times in a row!")

            if cls.current_session.correct_streak >= 3:
                # Bonus +1 Point when streak is 3+
                cls.current_session.points += 1

            if cls.current_session.correct_streak > cls.current_session.max_correct_streak: # Record max streak
                cls.current_session.max_correct_streak = cls.current_session.correct_streak
        else:
            cls.current_session.points -= 1 # Base point for incorrect answer
            cls.current_session.incorrect_answer += 1

            if cls.current_session.correct_streak >= 3:
                # Annouce end of streak if user has 3+ streak
                print(f"{cls.current_session} streaks has ended!")

            cls.current_session.correct_streak = 0
        
        # Calculate Accuracy
        cls.current_session.accuracy_percentage = round((cls.current_session.correct_answer / cls.current_session.question_answered) * 100)

        # Reset point if it went negative
        if cls.current_session.points < 0: cls.current_session.points = 0

    @classmethod
    def summarise_telemetry(cls) -> None:
        if cls.current_session is None:
            return
        if cls.current_session.active_user is not None:
            if not StateManager.debug_mode: # General result
                print(
                    f"{"="*50}\n"
                    f"Summary Report\n",
                    f"User: {cls.current_session.active_user.name}\n",
                    f"Earned {cls.current_session.points} points!\n",
                    f"Game mode: {cls.current_session.readable_operator}\n",
                    f"Time elapsed: {int(cls.current_session.time_elasped)} seconds\n\n",
                    f"Question answered: {cls.current_session.readable_question_answered}\n",
                    f"Accuracy: {cls.current_session.accuracy_percentage}% ({cls.current_session.correct_answer}/{cls.current_session.question_answered})\n",
                    f"Longest streak: {cls.current_session.max_correct_streak}\n",
                    f"Avg. Time/Question: {int(cls.current_session.average_time_per_question)} seconds\n",
                    f"{"="*50}"
                )
            else:
                print(
                    f"{"="*50}\n"
                    f"Summary Report for session {cls.current_session.id}.\n",
                    f"User: {cls.current_session.active_user.name} (user id: {cls.current_session.active_user.id})\n",
                    f"Earned {cls.current_session.points} points!\n",
                    f"Game mode: {cls.current_session.readable_operator} ({cls.current_session.operator.name})\n",
                    f"Time elapsed: {cls.current_session.time_elasped:.2f} seconds\n\n",
                    f"Question answered: {cls.current_session.readable_question_answered}\n",
                    f"Accuracy: {cls.current_session.accuracy_percentage}% ({cls.current_session.correct_answer}/{cls.current_session.question_answered})\n",
                    f"Longest streak: {cls.current_session.max_correct_streak}\n",
                    f"Avg. Time/Question: {cls.current_session.average_time_per_question:.2f} seconds\n",
                    f"{"="*50}"
                )
        else:
            print("Failed to generate a session summary report without any active user.")
