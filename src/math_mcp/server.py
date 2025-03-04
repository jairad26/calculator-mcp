from typing import Dict, List, Optional, Union, Any, Tuple
from mcp.server.fastmcp import FastMCP
import math
from .advanced_math import (
    factorial, 
    fibonacci, 
    calculate_statistics, 
    solve_quadratic,
    convert_angle,
    binary_operation,
    evaluate_expression,
    unary_operation,
    Operand
)

# Initialize FastMCP server
mcp = FastMCP("math")

# Basic arithmetic operations

@mcp.tool()
async def unary_operation(a: Operand, operation: str) -> Operand:
    """Perform a unary operation on a number.
    
    Args:
        a: The number to operate on. Can be an integer, float, or a string representing a constant (e.g., 'pi', 'e')
        operation: The operation to perform('sqrt')
    
    Returns:
        Result of the operation
    
    Raises:
        ValueError: If the operation is invalid
        TypeError: If the operation is not a string
    """
    return unary_operation(a, operation)

@mcp.tool()
async def binary_operation(a: Operand, b: Operand, operation: str) -> Operand:
    """Perform a basic arithmetic operation on two numbers.
    
    Args:
        a: First number. Can be an integer, float, or a string representing a constant (e.g., 'pi', 'e')
        b: Second number. Can be an integer, float, or a string representing a constant (e.g., 'pi', 'e')
        operation: The operation to perform('+', '-', '*', '/', '**')
    
    Returns:
        Result of the operation
    
    Raises:
        ValueError: If the operation is invalid or the second number is zero for division
    """
    return binary_operation(a, b, operation)

@mcp.tool()
async def calculate_expression(expression: str) -> Union[int, float]:
    """Evaluate a mathematical expression. The available operations are: +, -, *, /, **, sqrt.
    
    Args:
        expression: A string containing a mathematical expression (e.g., "2 + 3 * 4"). Can also include constants like 'pi' and 'e'.
    
    Returns:
        Result of the evaluated expression
    
    Raises:
        ValueError: If the expression is invalid or contains unauthorized functions
    """
    return evaluate_expression(expression)

# Advanced mathematical operations

@mcp.tool()
async def calc_factorial(n: int) -> int:
    """Calculate the factorial of a non-negative integer.
    
    Args:
        n: A non-negative integer
    
    Returns:
        The factorial of n (n!)
    
    Raises:
        ValueError: If n is negative
        TypeError: If n is not an integer
    """
    return factorial(n)

@mcp.tool()
async def calc_fibonacci(n: int) -> int:
    """Calculate the nth Fibonacci number.
    
    Args:
        n: A non-negative integer position in the Fibonacci sequence
    
    Returns:
        The nth Fibonacci number
    
    Raises:
        ValueError: If n is negative
        TypeError: If n is not an integer
    """
    return fibonacci(n)

@mcp.tool()
async def stats(numbers: List[Union[int, float]]) -> Dict[str, float]:
    """Calculate various statistical measures for a list of numbers.
    
    Args:
        numbers: A list of numbers
    
    Returns:
        A dictionary containing statistical measures (mean, median, mode, etc.)
    
    Raises:
        ValueError: If the input list is empty
    """
    return calculate_statistics(numbers)

@mcp.tool()
async def quadratic(a: float, b: float, c: float) -> Dict[str, Any]:
    """Solve a quadratic equation of the form ax² + bx + c = 0.
    
    Args:
        a: Coefficient of x²
        b: Coefficient of x
        c: Constant term
    
    Returns:
        A dictionary containing the solutions and equation details
    
    Raises:
        ValueError: If a is zero (making it a linear equation, not quadratic)
    """
    x1, x2 = solve_quadratic(a, b, c)
    
    # Format the result as a dictionary for better readability
    result = {
        "equation": f"{a}x² + {b}x + {c} = 0",
        "discriminant": b**2 - 4*a*c,
        "solutions": [
            complex(x1.real, x1.imag) if isinstance(x1, complex) else float(x1),
            complex(x2.real, x2.imag) if isinstance(x2, complex) else float(x2)
        ]
    }
    
    return result

@mcp.tool()
async def angle_convert(angle: float, from_unit: str, to_unit: str) -> Dict[str, Any]:
    """Convert an angle between different units (degrees, radians, gradians).
    
    Args:
        angle: The angle value to convert
        from_unit: The unit to convert from ('deg', 'rad', or 'grad')
        to_unit: The unit to convert to ('deg', 'rad', or 'grad')
    
    Returns:
        A dictionary containing the original and converted angle values
    
    Raises:
        ValueError: If invalid units are provided
    """
    converted = convert_angle(angle, from_unit, to_unit)
    
    return {
        "original": {
            "value": angle,
            "unit": from_unit
        },
        "converted": {
            "value": converted,
            "unit": to_unit
        }
    }

def main():
    """Entry point for the math MCP server."""
    mcp.run(transport='stdio')
    
if __name__ == "__main__":
    main() 