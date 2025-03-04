#!/usr/bin/env python3
"""
Test suite for the expression evaluator in advanced_math.py.
This script tests the functionality of the evaluate_expression function.
"""

import unittest
from src.math_mcp.advanced_math import evaluate_expression

class TestExpressionEvaluator(unittest.TestCase):
    """Test case for the expression evaluator."""
    
    def test_basic_arithmetic(self):
        """Test basic arithmetic operations."""
        # Addition
        self.assertEqual(evaluate_expression("2 + 3"), 5)
        self.assertEqual(evaluate_expression("2+3"), 5)
        
        # Subtraction
        self.assertEqual(evaluate_expression("5 - 2"), 3)
        self.assertEqual(evaluate_expression("5-2"), 3)
        
        # Multiplication
        self.assertEqual(evaluate_expression("4 * 3"), 12)
        self.assertEqual(evaluate_expression("4*3"), 12)
        
        # Division
        self.assertEqual(evaluate_expression("10 / 2"), 5)
        self.assertEqual(evaluate_expression("10/2"), 5)
        
        # Mixed operations
        self.assertEqual(evaluate_expression("2 + 3 * 4"), 14)
        self.assertEqual(evaluate_expression("(2 + 3) * 4"), 20)
    
    def test_exponentiation(self):
        """Test exponentiation operations."""
        self.assertEqual(evaluate_expression("2 ** 3"), 8)
        self.assertEqual(evaluate_expression("2**3"), 8)
        self.assertEqual(evaluate_expression("(2 + 1) ** 2"), 9)
        self.assertEqual(evaluate_expression("2 ** (1 + 2)"), 8)
    
    def test_sqrt_function(self):
        """Test square root function."""
        self.assertEqual(evaluate_expression("sqrt(4)"), 2)
        self.assertEqual(evaluate_expression("sqrt(9)"), 3)
        self.assertEqual(evaluate_expression("sqrt(2 + 2)"), 2)
        self.assertEqual(evaluate_expression("sqrt(3 ** 2)"), 3)
    
    def test_complex_expressions(self):
        """Test more complex expressions."""
        self.assertEqual(evaluate_expression("2 + 3 * 4 - 5"), 9)
        self.assertEqual(evaluate_expression("(2 + 3) * (4 - 1)"), 15)
        self.assertEqual(evaluate_expression("10 / (2 + 3)"), 2)
        self.assertEqual(evaluate_expression("2 ** 3 + 4"), 12)
        self.assertEqual(evaluate_expression("sqrt(16) + 2 ** 2"), 8)
        self.assertEqual(evaluate_expression("(sqrt(16) + 2) ** 2"), 36)
    
    def test_negative_numbers(self):
        """Test expressions with negative numbers."""
        self.assertEqual(evaluate_expression("-5 + 3"), -2)
        self.assertEqual(evaluate_expression("5 + -3"), 2)
        self.assertEqual(evaluate_expression("-5 * -3"), 15)
        self.assertEqual(evaluate_expression("5 * -3"), -15)
        self.assertEqual(evaluate_expression("-10 / 2"), -5)
        self.assertEqual(evaluate_expression("10 / -2"), -5)
    
    def test_error_handling(self):
        """Test error handling for invalid expressions."""
        # Empty expression
        with self.assertRaises(ValueError):
            evaluate_expression("")
        
        # Division by zero
        with self.assertRaises(ValueError):
            evaluate_expression("5 / 0")
        
        # Invalid operation
        with self.assertRaises(ValueError):
            evaluate_expression("5 ? 3")
        
        # Mismatched parentheses
        with self.assertRaises(ValueError):
            evaluate_expression("(2 + 3")
        
        with self.assertRaises(ValueError):
            evaluate_expression("2 + 3)")
        
        # Invalid sqrt usage
        with self.assertRaises(ValueError):
            evaluate_expression("sqrt 4")
        
        # Negative sqrt
        with self.assertRaises(ValueError):
            evaluate_expression("sqrt(-4)")

if __name__ == "__main__":
    unittest.main() 