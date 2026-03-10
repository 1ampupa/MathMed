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
        del self
