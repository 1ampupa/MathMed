class MathMedExceptions(Exception):
    """Base Exceptions for the MathMed program"""
    pass

class QuizGenerationExceededLimit(MathMedExceptions):
    """Raised when the quiz failed to generate within the generation attempt limits."""
    def __init__(self, message: str = "No valid quiz generated under this condition. Please change your quiz settings or revert to default settings."):
        self.message = message
        super().__init__(self.message)

class UnknownSessionPresetIdentifier(MathMedExceptions):
    """Raised when the game tried to access an unknown game preset."""
    def __init__(self, message: str = "Unknown Session Preset Identifier"):
        self.message = message
        super().__init__(self.message)
