import traceback
from module.core.utils.operators import Operators
from module.core.utils.state import State, StateManager
from module.core.user.user import User

class Session:
    session_id_counter = 1

    def __init__(self, Operators: Operators) -> None:
        self.id = Session.session_id_counter
        self.active_users: list[User] = []
        self.operator: Operators = Operators
        self.readable_operator: str = Operators.readable()

        # Telemetry
        self.question_answered: int = 0
        self.points: int = 0
        self.correct_answer: int = 0
        self.incorrect_answer: int = 0
        self.correct_streak: int = 0
        self.max_correct_streak: int = 0
        self.accuracy_percentage: int = 0
        self.time_elapsed: float = 0
        self.average_time_per_question: float = 0
        self.five_recent_answer_results: list = []

        Session.session_id_counter += 1

    @property
    def readable_question_answered(self) -> str:
        if self.question_answered == 1:
            return f'1 question'
        else:
            return f'{self.question_answered} questions'

    from module.core.user.user import User
    def connect_user(self, user: User) -> None:
        if len(self.active_users) >= 1: # Preventing overlapping users in the same session
            print(f"This session is occupied")
            return
        
        if user.current_session is not None: # Preventing user joining multiple sessions
            print(f"This user is already in the other session ({user.current_session.id}).")
            return
        
        self.active_users.append(user)
        user.connect_session(self)

        if StateManager.debug_mode:
            print(f"Connecting {user.name} to the session... (id: {self.id})")
        else:
            print(f"Connecting {user.name} to the session...")

    def disconnect_user(self, user: User) -> None:
        if user.current_state != State.IN_SESSION:
            print("Currently not in any session.")
            return
        
        if self.active_users is None:
            print("There's no active user in this session.")
            return
        
        if StateManager.debug_mode:
            print(f"Disconnecting {user} from the session (id: {self.id}).")
        else:
            print(f"Disconnecting {user} from the session.")

        self.disconnect_user(user)
        self.active_users.remove(user)

    def end_session(self) -> None:
        from module.core.session.session_telemetry import SessionTelemetry
        # Calculate Accuracy
        for user in self.active_users:
            if self.question_answered != 0:
                self.average_time_per_question = self.time_elapsed / self.question_answered
                print("Generating your summary report...")
                # Creating telemetry summary report
                SessionTelemetry.summarise_telemetry(self, user)
            else:
                print("Session abandoned; No summary report generated.")

        # Disconnect
        if self.active_users is not None:
            for user in self.active_users:
                user.disconnect_session()
        
        if StateManager.debug_mode: print(f"Ended session (id: {self.id})")

    def start(self) -> None:
        # Check Process

        # Check client state
        for user in self.active_users:
            if user.current_state != State.IN_SESSION:
                print("Client is not in any session.")
                return
        
        # Check user in session
        if not self.active_users:
            print("Cannot start a session without any user.")
            return

        print("Answer the questions correctly.\nType 'q' to exit the game.")

        # Game loop
        from module.core.session.session_loop import SessionLoop

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
                input("Press Enter Button to return to main menu.")
                break
