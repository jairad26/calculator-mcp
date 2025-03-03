#!/usr/bin/env python3
"""
Test suite for the Calculator MCP Server.
This script tests the functionality of the calculator tools.
"""

import unittest
import asyncio
import subprocess
import time
import os
import signal
from mcp.client import Client

class TestCalculatorMCP(unittest.TestCase):
    """Test case for the Calculator MCP Server."""
    
    @classmethod
    def setUpClass(cls):
        """Start the calculator MCP server as a subprocess."""
        # Start the server process
        cls.server_process = subprocess.Popen(
            ["python", "calculator_mcp.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE,
            text=True,
            bufsize=1
        )
        # Give the server a moment to start up
        time.sleep(1)
        
        # Create the client
        cls.client = Client(transport="stdio", command=["python", "src/calculator_mcp/calculator_mcp.py"])
    
    @classmethod
    def tearDownClass(cls):
        """Terminate the calculator MCP server subprocess."""
        # Close the client
        asyncio.run(cls.client.close())
        
        # Terminate the server process
        cls.server_process.terminate()
        try:
            cls.server_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            cls.server_process.kill()
    
    def test_basic_arithmetic(self):
        """Test basic arithmetic operations."""
        # Test addition
        result = asyncio.run(self.client.add(5, 3))
        self.assertEqual(result, 8)
        
        # Test subtraction
        result = asyncio.run(self.client.subtract(10, 4))
        self.assertEqual(result, 6)
        
        # Test multiplication
        result = asyncio.run(self.client.multiply(6, 7))
        self.assertEqual(result, 42)
        
        # Test division
        result = asyncio.run(self.client.divide(20, 5))
        self.assertEqual(result, 4)
    
    def test_advanced_operations(self):
        """Test advanced mathematical operations."""
        # Test power
        result = asyncio.run(self.client.power(2, 8))
        self.assertEqual(result, 256)
        
        # Test square root
        result = asyncio.run(self.client.square_root(144))
        self.assertEqual(result, 12)
        
        # Test expression evaluation
        result = asyncio.run(self.client.calculate_expression("2 * (3 + 4)"))
        self.assertEqual(result, 14)
    
    def test_factorial(self):
        """Test factorial calculation."""
        result = asyncio.run(self.client.calc_factorial(5))
        self.assertEqual(result, 120)
        
        result = asyncio.run(self.client.calc_factorial(0))
        self.assertEqual(result, 1)
    
    def test_fibonacci(self):
        """Test Fibonacci sequence calculation."""
        result = asyncio.run(self.client.calc_fibonacci(10))
        self.assertEqual(result, 55)
        
        result = asyncio.run(self.client.calc_fibonacci(0))
        self.assertEqual(result, 0)
        
        result = asyncio.run(self.client.calc_fibonacci(1))
        self.assertEqual(result, 1)
    
    def test_statistics(self):
        """Test statistical calculations."""
        numbers = [4, 7, 2, 9, 3, 5, 8, 6, 1]
        result = asyncio.run(self.client.stats(numbers))
        
        self.assertEqual(result["mean"], 5)
        self.assertEqual(result["median"], 5)
        self.assertEqual(result["min"], 1)
        self.assertEqual(result["max"], 9)
        self.assertEqual(result["range"], 8)
    
    def test_quadratic(self):
        """Test quadratic equation solver."""
        # Test with real solutions
        a, b, c = 1, -3, 2  # x² - 3x + 2 = 0, solutions: x = 1, x = 2
        result = asyncio.run(self.client.quadratic(a, b, c))
        
        self.assertEqual(result["discriminant"], 1)
        solutions = [float(sol) for sol in result["solutions"]]
        self.assertIn(1.0, solutions)
        self.assertIn(2.0, solutions)
        
        # Test with complex solutions
        a, b, c = 1, 2, 5  # x² + 2x + 5 = 0, complex solutions
        result = asyncio.run(self.client.quadratic(a, b, c))
        
        self.assertLess(result["discriminant"], 0)  # Discriminant should be negative
        
        # Extract real and imaginary parts from the complex solutions
        solutions = result["solutions"]
        self.assertEqual(len(solutions), 2)
        
        # Check if solutions are complex
        self.assertTrue(isinstance(solutions[0], dict) or isinstance(solutions[0], complex))
        self.assertTrue(isinstance(solutions[1], dict) or isinstance(solutions[1], complex))
        
        # Get real and imaginary parts based on the format
        if isinstance(solutions[0], dict):
            # If solutions are returned as dictionaries with real/imag keys
            z1_real = solutions[0]["real"]
            z1_imag = solutions[0]["imag"]
            z2_real = solutions[1]["real"]
            z2_imag = solutions[1]["imag"]
        elif isinstance(solutions[0], complex):
            # If solutions are returned as complex objects
            z1_real = solutions[0].real
            z1_imag = solutions[0].imag
            z2_real = solutions[1].real
            z2_imag = solutions[1].imag
        else:
            # If solutions are returned in another format (e.g., as strings)
            # Parse them accordingly
            self.fail("Unexpected format for complex solutions")
        
        # Check that solutions are complex conjugates
        self.assertAlmostEqual(z1_real, z2_real)
        self.assertAlmostEqual(z1_imag, -z2_imag)
    
    def test_angle_conversion(self):
        """Test angle unit conversion."""
        # Test degrees to radians
        result = asyncio.run(self.client.angle_convert(180, "deg", "rad"))
        self.assertAlmostEqual(result["converted"]["value"], 3.141592653589793, places=10)
        
        # Test radians to degrees
        result = asyncio.run(self.client.angle_convert(3.141592653589793, "rad", "deg"))
        self.assertAlmostEqual(result["converted"]["value"], 180, places=10)
    
    def test_error_handling(self):
        """Test error handling for invalid inputs."""
        # Test division by zero
        with self.assertRaises(Exception):
            asyncio.run(self.client.divide(10, 0))
        
        # Test square root of negative number
        with self.assertRaises(Exception):
            asyncio.run(self.client.square_root(-1))
        
        # Test factorial of negative number
        with self.assertRaises(Exception):
            asyncio.run(self.client.calc_factorial(-5))

if __name__ == "__main__":
    unittest.main() 