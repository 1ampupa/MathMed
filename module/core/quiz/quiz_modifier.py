from module.core.utils.operators import Operators

class QuizModifier():
    
    def __init__(self) -> None:
        # Default Settings
        self.rules: dict[Operators, dict] = self.use_default_settings()  

    def use_default_settings(self) -> dict[Operators, dict]:
        return {
            Operators.ADDITION: {
                "allow_duplicate": True,    # a + a
                "allow_zero": False         # a + 0 | 0 + a | 0 + 0
            },  
            Operators.SUBTRACTION: {    
                "allow_equal": False,       # a - a
                "allow_negative": False,    # a - b, b > a
                "allow_zero": False         # a - 0
            },  
            Operators.MULTIPLICATION: { 
                "allow_square": True,       # a * a
                "allow_zero": False,        # a * 0 | 0 * a | 0 * 0
                "allow_one": False          # a * 1 | 1 * a | 1 * 1
            },
            Operators.DIVISION: {
                "allow_equal": False,       # a / a
                "allow_zero": False,        # 0 / a
                "allow_one": False          # a / 1
            }  
        }
