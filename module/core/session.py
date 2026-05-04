import time, traceback
from module.core.operators import Operators
from module.core.state import State, StateManager

class Session:
    session_id_counter = 1

    def __init__(self, Operators: Operators) -> None:
        self.id = Session.session_id_counter
        self.active_user = None
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
        self.time_elasped: float = 0
        self.average_time_per_question: float = 0
        self.five_recent_answer_results: list = []

        Session.session_id_counter += 1

    @property
    def readable_question_answered(self) -> str:
        if self.question_answered == 1:
            return f'1 question'
        else:
            return f'{self.question_answered} questions'

    def connect_user(self, user) -> None:
        if self.active_user is not None: # Preventing overlapping users in the same session
            print(f"This session is occupied by {self.active_user.name}")
            return
        
        if user.current_session is not None: # Preventing user joining multiple sessions
            print(f"This user is already in the other session ({user.current_session.id}).")
            return
        
        StateManager.change_state(State.IN_SESSION)
        self.active_user = user
        user.current_session = self
        if StateManager.debug_mode:
            print(f"Connecting {user.name} to the session... (id: {self.id})")
        else:
            print(f"Connecting {user.name} to the session...")

    def disconnect_user(self) -> None:
        if StateManager.current_state != State.IN_SESSION:
            print("Currently not in any session.")
            return
        
        if self.active_user is None:
            return
        
        # Calculate Accuracy
        from module.core.session_telemetry import SessionTelemetry
        if self.question_answered != 0:
            self.average_time_per_question = self.time_elasped / self.question_answered
            # Creating telemetry summary report
            SessionTelemetry.summarise_telemetry()
        else:
            print("Session abandoned; No summary report generated.")

        if StateManager.debug_mode: print(f"Disconnecting {self.active_user.name} from session {self.id}.")
        self.active_user.current_session = None
        self.active_user = None
        StateManager.change_state(State.MAIN_MENU)
        if StateManager.debug_mode: print(f"Ended session {self.id}")

    def start(self) -> None:
        # Check Process

        # Check client state
        if StateManager.current_state != State.IN_SESSION:
            print("Client is not in any session.")
            return
        
        # Check user in session
        if self.active_user is None:
            print("Cannot start a session without any user.")
            return
        
        from module.core.quiz import Quiz
        from module.core.user_answer import UserAnswer

        print("Answer the questions correctly.\n")

        # Game loop
        from module.core.session_telemetry import SessionTelemetry
        SessionTelemetry.current_session = self
        while True:
            try:
                # Generate Quiz
                quiz = Quiz.generate(self.active_user, self.operator)
                print(quiz)

                # Start Quiz Timer
                quiz_start_time = time.perf_counter()

                # Receive User Answer
                answer = input("Answer for world peace: ")

                # Game Quit Handler (temporary)
                if answer.strip().lower() == 'q':
                    self.disconnect_user()
                    StateManager.change_state(State.MAIN_MENU)
                    print("You quit the game. Thanks for saving world peace.")
                    break
                
                quiz_time_taken = time.perf_counter() - quiz_start_time

                # Check User Answer
                try:
                    result = UserAnswer(self.active_user, quiz, int(answer))
                except ValueError:
                    print("Invalid input, please answer the question using only numbers.")
                    continue

                print(f"{result}! The answer is {result.quiz.answer}.\n")

                # Update Telemetry and difficulty
                SessionTelemetry.update_telemetry(result.is_correct, quiz_time_taken)
                result.update_difficulty()

                # Pop the last index of the five recent performance counter if its length reaches 5
                if len(self.five_recent_answer_results) >= 5:
                    self.five_recent_answer_results.pop()

            except Exception as e:
                self.disconnect_user()
                StateManager.change_state(State.MAIN_MENU)
                if StateManager.debug_mode:
                    print(f"A fatal error occurred, and the session was ended unexpectedly with the following error message:\n")
                    traceback.print_exc()
                else:
                    print(f"A fatal error occurred, and the session was ended unexpectedly with the following error message:\n{e}")     
                input("Press Enter Button to return to main menu.")
                break
