from module.core.user import User

class UserTelemetry:
    def __init__(self, user: User) -> None:
        self.user = user

        # Session Telemetry
        self.session = None


    @classmethod
    def connect_user(cls, user: User) -> UserTelemetry:
        if not User: raise Exception("User not exist.")
        return cls(user)

    def disconnect_user(self, user: User) -> None:
        self.user = None
