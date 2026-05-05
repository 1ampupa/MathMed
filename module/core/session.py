import traceback
from module.core.operators import Operators
from module.core.state import State, StateManager

class Session:
    _session_id_counter = 1

    def __init__(self, Operators: Operators) -> None:
        self.id: str = f"session_{Session._session_id_counter}"
        self.active_users: list = []
        self.operator: Operators = Operators
        self.readable_operator: str = Operators.readable()

        # Session Settings
        self.max_active_users: int = 1
        self.min_questions_for_report: int = 3

        # Session Telemetry
        self.all_question_answered: int = 0

        Session._session_id_counter += 1

    # Telemetry
    def summarise_user_performance(self, user):
        from module.core.session_telemetry import SessionTelemetry

        # Generate report
        if (self.all_question_answered >= self.min_questions_for_report
            and user.question_answered >= self.min_questions_for_report):     
            # Calculate Accuracy for each player
            user.average_time_per_question = user.time_elapsed / user.question_answered
            print("Generating your summary report...")
            # Creating telemetry summary report
            SessionTelemetry.summarise_telemetry(self, user)
        else:
            print("Session abandoned; No summary report generated.")

    # Connection

    def connect_user(self, user) -> None:
        if len(self.active_users) == self.max_active_users:
            print(f"Can't connect {user.name} to the session (id: {self.id}); The session is full. (Max: {self.max_active_users})")
            return     
        
        user.connect_session(self)
        self.active_users.append(user)
    
    def disconnect_user(self, user) -> None:
        if user not in self.active_users:
            print(f"The user is not in this session")
            return

        self.summarise_user_performance(user)
        self.active_users.remove(user)
        user.disconnect_session(self)

    def end_session(self) -> None:
        for user in self.active_users:
            self.summarise_user_performance(user)

        # Disconnect
        if self.active_users is not None:
            for user in self.active_users:
                user.disconnect_session(self)
            self.active_users = []

        print(f"Ended session (id: {self.id})")

    # Game loop

    def start(self) -> None:
        # Check Process
        # Check client state
        if StateManager.current_state != State.IN_SESSION:
            print("Client is not in any session.")
            return
        
        # Check user in session
        if self.active_users is None:
            print("Cannot start a session without any user.")
            return

        print("Answer the questions correctly.\nType 'q' to exit the game.")

        # Game loop
        from module.core.session_loop import SessionLoop

        while True:
            try:
                looping = SessionLoop.loop(self)
                if not looping: break
            except Exception as e:
                if StateManager.debug_mode:
                    print(f"A fatal error occurred, and the session was ended unexpectedly with the following error message:\n")
                    traceback.print_exc()
                else:
                    print(f"A fatal error occurred, and the session was ended unexpectedly with the following error message:\n{e}")
                self.end_session()
                input("Press Enter Button to exit the program.")
                break
