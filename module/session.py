import time
from module.operator import Operator

class Session:
    session_id_counter = 1

    def __init__(self) -> None:
        self.id = Session.session_id_counter
        self.active_user = None

        # Telemetry
        self.question_answered = 0
        self.points = 0
        self.correct_answer = 0
        self.incorrect_answer = 0
        self.correct_streak = 0
        self.max_correct_streak = 0
        self.accuracy_percentage = 0
        self.time_elasped = 0
        self.average_time_per_question = 0

        Session.session_id_counter += 1

    def connect_user(self, user):
        if self.active_user is not None: # Preventing overlapping users in the same session
            print(f"This session is occupied by {self.active_user.name}")
            return
        
        if user.current_session is not None:    
            print(f"This user is already in the other session ({user.current_session.id}).")
            return
        self.active_user = user
        user.current_session = self
        print(f"Connecting {user.name} to the session {self.id}")

    def disconnect_user(self):
        if self.active_user is not None:
            # Calculate Accuracy and
            if self.question_answered != 0:
                self.accuracy_percentage = round((self.correct_answer / self.question_answered) * 100)
                self.average_time_per_question = self.time_elasped / self.question_answered
                # Creating telemetry summary report
                self.summarise_telemetry()
            else:
                print("Session abandoned; No summary report generated.")
            
            print(f"Disconnecting {self.active_user.name} from session {self.id}.")
            self.active_user.current_session = None
        self.active_user = None
        print(f"Ended session {self.id}")

    def start(self):
        if self.active_user is None:
            print("Cannot start a session without any user.")
            return
        
        from module.quiz import Quiz
        from module.user_answer import UserAnswer

        
        print("Session is ready!\nAnswer the questions correctly.\n")

        while True:
            # Generate Quiz
            quiz = Quiz.generate(self.active_user, Operator.MULTIPLICATION)
            print(quiz)

            # Start Quiz Timer
            quiz_start_time = time.perf_counter()

            # Receive User Answer
            answer = input("Answer for world peace: ")

            # Game Quit Handler (temporary)
            if answer.strip().lower() == 'q':
                self.disconnect_user()
                print("You quit the game. Thanks for saving world peace.")
                break
            
            quiz_time_taken = time.perf_counter() - quiz_start_time

            # Check User Answer
            try:
                result = UserAnswer(self.active_user, quiz, int(answer))
            except ValueError:
                print("Invalid input, please answer the question using only numbers.")
                continue
            result.update_difficulty()

            print(f"{result}! The answer is {result.quiz.answer}.\n")

            self.update_telemetry(result.is_correct, quiz_time_taken)

    def update_telemetry(self, is_correct: bool, time_elapsed: float) -> None:
        # Update Statstic
        self.question_answered += 1
        self.time_elasped += time_elapsed

        if is_correct:
            self.points += 1 # Base point for correct answer
            self.correct_answer += 1
            self.correct_streak += 1

            if self.correct_streak % 3 == 0:
                # Annouce streak every 3 correct answers
                print(f"Correct {self.correct_streak} times in a row!")

            if self.correct_streak >= 3:
                # Bonus +1 Point when streak is 3+
                self.points += 1

            if self.correct_streak > self.max_correct_streak: # Record max streak
                self.max_correct_streak = self.correct_streak
        else:
            self.points -= 1 # Base point for incorrect answer
            self.incorrect_answer += 1

            if self.correct_streak >= 3:
                # Annouce end of streak if user has 3+ streak
                print("Streak ended!")

            self.correct_streak = 0
    
    def summarise_telemetry(self) -> None:
        if self.active_user is not None:
            print(
                f"{"="*50}\n"
                f"Session Summary Report for session {self.id}\n",
                f"User: {self.active_user.name}\n",
                f"{self.points} Points!\n",
                f"Time elapsed: {self.time_elasped:.2f} seconds\n\n",
                f"Question answered: {self.question_answered}\n",
                f"Accuracy: {self.accuracy_percentage} % ({self.correct_answer}/{self.question_answered})\n",
                f"Max streak: {self.max_correct_streak}\n",
                f"Avg. Time/Question: {self.average_time_per_question:.2f} seconds\n",
                f"{"="*50}"
            )
        else:
            print("Failed to generate a session summary report without any active user.")
