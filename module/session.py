from module.operator import Operator

class Session:
    session_id_counter = 1

    def __init__(self) -> None:
        self.id = Session.session_id_counter
        self.active_user = None

        # Telemetry
        self.question_answered = 0
        self.correct_answer = 0
        self.incorrect_answer = 0
        self.correct_streak = 0
        self.max_correct_streak = 0
        self.accuracy_percentage = 100
        self.time_per_question = 0

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
        print(f"{user.name} added to the session {self.id}")

    def disconnect_user(self):
        if self.active_user is not None:
            print(f"{self.active_user.name} is being disconnected from session {self.id}.")
            self.active_user.current_session = None
        self.active_user = None
        print(f"Ended session {self.id}")

    def start(self):
        if self.active_user is None:
            print("Cannot start a session without any user.")
            return
        
        from module.quiz import Quiz
        from module.user_answer import UserAnswer
        
        while True:
            quiz = Quiz.generate(self.active_user, Operator.MULTIPLICATION)
            print(quiz)

            answer = input("Answer for world peace: ")
            if answer.strip().lower() == 'q':
                self.disconnect_user()
                print("You quit the game. Thanks for saving world peace.")
                break
            
            try:
                result = UserAnswer(self.active_user, quiz, int(answer))
            except ValueError:
                print("Invalid input, please answer the question using only numbers.")
                continue
            result.update_difficulty()

            print(f"{result}! The answer is {result.quiz.answer}.\n")
    