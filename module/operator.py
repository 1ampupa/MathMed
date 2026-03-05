from enum import Enum, auto

class Operator(Enum):
    ADDITION = "+"
    SUBTRACTION = "-"
    MULTIPLICATION = "*"
    DIVISION = "/"

    def apply(self: Operator, a: int, b: int) -> int:
        if self is Operator.ADDITION:
            return a + b
        elif self is Operator.SUBTRACTION:
            return a - b
        elif self is Operator.MULTIPLICATION:
            return a * b
        elif self is Operator.DIVISION:
            return int(a / b)