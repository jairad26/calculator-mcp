"""
Advanced mathematical operations for the Calculator MCP Server.
This module provides more complex mathematical functions beyond basic arithmetic.
"""

import math
import statistics
from typing import List, Union, Tuple, Dict, Any

Operand = Union[int, float, str]

def unary_operation(a: Operand, operation: str) -> Operand:
    if isinstance(a, str):
        if a == 'pi':
            a = math.pi
        elif a == 'e':
            a = math.e
        else:
            raise ValueError(f"Invalid operand: {a}")

    if operation == 'sqrt':
        if a < 0:
            raise ValueError("Cannot calculate square root of a negative number")
        return math.sqrt(a)
    else:
        raise ValueError("Invalid operation")

def binary_operation(a: Operand, b: Operand, operation: str) -> Operand:
    if isinstance(a, str):
        if a == 'pi':
            a = math.pi
        elif a == 'e':
            a = math.e
        else:
            raise ValueError(f"Invalid operand: {a}")
    if isinstance(b, str):
        if b == 'pi':
            b = math.pi
        elif b == 'e':
            b = math.e
        else:
            raise ValueError(f"Invalid operand: {b}")

    if operation == '+':
        return a + b
    elif operation == '-':
        return a - b
    elif operation == '*':
        return a * b
    elif operation == '/':
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b
    elif operation == '**':
        return a ** b
    elif operation == 'log':
        if a <= 0 or a == 1:
            raise ValueError("Log base must be positive and not equal to 1")
        if b <= 0:
            raise ValueError("Cannot calculate logarithm of a non-positive number")
        return math.log(b, a)  # In Python, log(value, base)
    else:
        raise ValueError("Invalid operation")
    
def evaluate_expression(expression: str) -> float:
    # Remove all whitespace
    expression = expression.replace(" ", "")
    
    if not expression:
        raise ValueError("Empty expression")
    
    # Parse the expression
    def parse_expression(expr, pos=0):
        """Parse an expression starting at the given position."""
        result, pos = parse_term(expr, pos)
        
        while pos < len(expr) and expr[pos] in ('+', '-'):
            op = expr[pos]
            pos += 1
            right, pos = parse_term(expr, pos)
            result = binary_operation(result, right, op)
            
        return result, pos
    
    def parse_term(expr, pos):
        """Parse a term (product or quotient) starting at the given position."""
        result, pos = parse_factor(expr, pos)
        
        while pos < len(expr) and expr[pos] in ('*', '/'):
            op = expr[pos]
            pos += 1
            right, pos = parse_factor(expr, pos)
            result = binary_operation(result, right, op)
            
        return result, pos
    
    def parse_factor(expr, pos):
        """Parse a factor (number, parenthesized expression, or function) starting at the given position."""
        # Check for unary operations
        if pos < len(expr) and expr[pos:pos+4] == 'sqrt':
            pos += 4
            if pos < len(expr) and expr[pos] == '(':
                pos += 1
                arg, pos = parse_expression(expr, pos)
                if pos < len(expr) and expr[pos] == ')':
                    pos += 1
                    return unary_operation(arg, 'sqrt'), pos
                else:
                    raise ValueError("Missing closing parenthesis for sqrt function")
            else:
                raise ValueError("sqrt function requires parentheses")
        elif pos < len(expr) and expr[pos:pos+3] == 'log':
            pos += 3
            if pos < len(expr) and expr[pos] == '(':
                pos += 1
                base, pos = parse_expression(expr, pos)
                if pos < len(expr) and expr[pos] == ',':
                    pos += 1
                    value, pos = parse_expression(expr, pos)
                    if pos < len(expr) and expr[pos] == ')':
                        pos += 1
                        return binary_operation(value, base, 'log'), pos
                    else:
                        raise ValueError("Missing closing parenthesis for log function")
                else:
                    raise ValueError("log function requires two arguments separated by a comma")
            else:
                raise ValueError("log function requires parentheses")
                    
        
        # Check for parenthesized expressions
        if pos < len(expr) and expr[pos] == '(':
            pos += 1
            result, pos = parse_expression(expr, pos)
            if pos < len(expr) and expr[pos] == ')':
                pos += 1
                
                # Check for exponentiation after parentheses
                if pos + 1 < len(expr) and expr[pos:pos+2] == '**':
                    pos += 2
                    exponent, pos = parse_factor(expr, pos)
                    result = binary_operation(result, exponent, '**')
                
                return result, pos
            else:
                raise ValueError("Missing closing parenthesis")
        
        # Parse a number
        start = pos
        # Handle negative numbers
        if pos < len(expr) and expr[pos] == '-':
            pos += 1
            
        # Parse digits and decimal point
        while pos < len(expr) and (expr[pos].isdigit() or expr[pos] == '.'):
            pos += 1
            
        if start == pos:
            raise ValueError(f"Expected number at position {pos}")
            
        try:
            num = float(expr[start:pos])
            # Convert to int if it's a whole number
            if num.is_integer():
                num = int(num)
        except ValueError:
            raise ValueError(f"Invalid number format: {expr[start:pos]}")
        
        # Check for exponentiation
        if pos + 1 < len(expr) and expr[pos:pos+2] == '**':
            pos += 2
            exponent, pos = parse_factor(expr, pos)
            num = binary_operation(num, exponent, '**')
            
        return num, pos
    
    # Start parsing from the beginning
    try:
        result, pos = parse_expression(expression)
        if pos < len(expression):
            raise ValueError(f"Unexpected character at position {pos}: '{expression[pos]}'")
        return result
    except Exception as e:
        if isinstance(e, ValueError):
            raise
        else:
            raise ValueError(f"Error evaluating expression: {str(e)}")

def factorial(n: int) -> int:
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)

def fibonacci(n: int) -> int:
    if n < 0:
        raise ValueError("Fibonacci is not defined for negative indices")
    if n <= 1:
        return n
    
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

def calculate_statistics(numbers: List[Union[int, float]]) -> Dict[str, float]:
    if not numbers:
        raise ValueError("Cannot calculate statistics on an empty list")
    
    result = {
        "mean": statistics.mean(numbers),
        "median": statistics.median(numbers),
        "min": min(numbers),
        "max": max(numbers),
        "range": max(numbers) - min(numbers),
    }
    
    # Mode can raise StatisticsError if no unique mode
    try:
        result["mode"] = statistics.mode(numbers)
    except statistics.StatisticsError:
        # If no unique mode, return None
        result["mode"] = None
    
    # Variance and standard deviation require at least 2 values
    if len(numbers) > 1:
        result["variance"] = statistics.variance(numbers)
        result["std_dev"] = statistics.stdev(numbers)
    else:
        result["variance"] = 0
        result["std_dev"] = 0
    
    return result

def solve_quadratic(a: float, b: float, c: float) -> Tuple[Union[float, complex], Union[float, complex]]:
    if a == 0:
        raise ValueError("Coefficient 'a' cannot be zero in a quadratic equation")
    
    # Calculate the discriminant
    discriminant = b**2 - 4*a*c
    
    # Calculate the two solutions
    if discriminant >= 0:
        # Real solutions
        x1 = (-b + math.sqrt(discriminant)) / (2*a)
        x2 = (-b - math.sqrt(discriminant)) / (2*a)
    else:
        # Complex solutions
        real_part = -b / (2*a)
        imag_part = math.sqrt(abs(discriminant)) / (2*a)
        x1 = complex(real_part, imag_part)
        x2 = complex(real_part, -imag_part)
    
    return (x1, x2)

def convert_angle(angle: float, from_unit: str, to_unit: str) -> float:
    # Validate units
    valid_units = {'deg', 'rad', 'grad'}
    if from_unit not in valid_units or to_unit not in valid_units:
        raise ValueError(f"Units must be one of: {', '.join(valid_units)}")
    
    # Convert to radians first (as an intermediate step)
    if from_unit == 'deg':
        radians = math.radians(angle)
    elif from_unit == 'grad':
        radians = angle * (math.pi / 200)
    else:  # from_unit == 'rad'
        radians = angle
    
    # Convert from radians to the target unit
    if to_unit == 'deg':
        return math.degrees(radians)
    elif to_unit == 'grad':
        return radians * (200 / math.pi)
    else:  # to_unit == 'rad'
        return radians 
    
def trigonometric_operation(angle: float, operation: str) -> float:
    if operation == 'sin':
        return math.sin(angle)
    elif operation == 'cos':
        return math.cos(angle)
    elif operation == 'tan':
        return math.tan(angle)
    else:
        raise ValueError("Invalid operation")
    
def hyperbolic_operation(angle: float, operation: str) -> float:
    if operation == 'sinh':
        return math.sinh(angle)
    elif operation == 'cosh':
        return math.cosh(angle)
    elif operation == 'tanh':
        return math.tanh(angle)
    else:
        raise ValueError("Invalid operation")
    