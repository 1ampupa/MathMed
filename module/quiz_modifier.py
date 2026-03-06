class QuizModifier():
    # Default Settings

    allow_duplicate_addends = True         # a + a
    allow_zero_addend = False              # a + 0 | 0 + a | 0 + 0
    
    allow_equal_subtraction = False        # a - a
    allow_negative_subtraction = False     # a - b, b > a
    allow_zero_subtrahend = False          # a - 0
    
    allow_square_multiplication = True     # a * a
    allow_zero_factor = False              # a * 0 | 0 * a | 0 * 0
    allow_one_factor = False               # a * 1 | 1 * a | 1 * 1
    
    allow_dividend_equal_divisor = False   # a / a
    allow_zero_dividend = False            # 0 / a
    allow_one_divisor = False              # a / 1
