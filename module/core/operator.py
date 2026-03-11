from enum import Enum

class Operator(Enum):
    
    # OPERATOR
    ADDITION = "+"
    SUBTRACTION = "-"
    MULTIPLICATION = "×"
    DIVISION = "÷"

    def apply(self: Operator, a: int, b: int) -> int:
        if self is Operator.ADDITION:
            return a + b
        elif self is Operator.SUBTRACTION:
            return a - b
        elif self is Operator.MULTIPLICATION:
            return a * b
        elif self is Operator.DIVISION:
            return int(a / b)
        
    def readable(self) -> str:
        match self:
            case Operator.ADDITION: return Operator.ADDITION.value
            case Operator.SUBTRACTION: return Operator.SUBTRACTION.value
            case Operator.MULTIPLICATION: return Operator.MULTIPLICATION.value
            case Operator.DIVISION: return Operator.DIVISION.value
            case _: raise RuntimeError("No operator for this session")