from module.core.user.user import User

class UserTelemetry:
    def __init__(self, user: User) -> None:
        self.user = user
        