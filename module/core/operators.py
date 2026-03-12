from enum import Enum

class Operators(Enum):
    
    # OPERATOR
    ADDITION = "+"
    SUBTRACTION = "-"
    MULTIPLICATION = "×"
    DIVISION = "÷"

    def apply(self: Operators, a: int, b: int) -> int:
        if self is Operators.ADDITION:
            return a + b
        elif self is Operators.SUBTRACTION:
            return a - b
        elif self is Operators.MULTIPLICATION:
            return a * b
        elif self is Operators.DIVISION:
            return int(a / b)
        
    def readable(self) -> str:
        match self:
            case Operators.ADDITION: return Operators.ADDITION.value
            case Operators.SUBTRACTION: return Operators.SUBTRACTION.value
            case Operators.MULTIPLICATION: return Operators.MULTIPLICATION.value
            case Operators.DIVISION: return Operators.DIVISION.value
            case _: raise RuntimeError("No operator for this session")