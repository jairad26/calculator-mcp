# Calculator MCP Server

A simple MCP (Model-Calling Protocol) server that provides mathematical calculation tools.

## Features

- Basic arithmetic operations (add, subtract, multiply, divide)
- Advanced mathematical functions (power, square root)
- Expression evaluation with safety restrictions
  - Supports complex expressions with parentheses
  - Handles operator precedence correctly
  - Supports functions like sqrt()
- Statistical calculations (mean, median, mode, variance, etc.)
- Special mathematical functions (factorial, Fibonacci)
- Equation solving (quadratic equations)
- Unit conversions (angle units)
- Easily extensible for additional mathematical operations

## Installation

1. Clone this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

### Running the Server

You can run the server directly:

```bash
python calculator_mcp.py
```

Or with HTTP transport:

```bash
python calculator_mcp.py --transport http --host localhost --port 8000
```

### Server Management

Use the run_server.py script for more advanced server management:

```bash
# Start the server with stdio transport (default)
python run_server.py

# Start the server with HTTP transport
python run_server.py --transport http --host localhost --port 8000

# Run as a daemon in the background
python run_server.py --daemon --log-file calculator.log

# Check server status
python run_server.py --status

# Stop the server
python run_server.py --stop

# Restart the server
python run_server.py --restart
```

### Available Tools

The server provides the following mathematical tools:

#### Basic Operations
- `add(a, b)`: Add two numbers
- `subtract(a, b)`: Subtract b from a
- `multiply(a, b)`: Multiply two numbers
- `divide(a, b)`: Divide a by b
- `power(base, exponent)`: Raise base to the power of exponent
- `square_root(number)`: Calculate the square root of a number
- `calculate_expression(expression)`: Evaluate a mathematical expression string

#### Expression Evaluation
The `calculate_expression` tool supports complex mathematical expressions including:
- Basic arithmetic: `2 + 3 * 4`
- Parentheses for grouping: `(2 + 3) * 4`
- Exponentiation: `2 ** 3`
- Square root function: `sqrt(16)`
- Nested expressions: `sqrt(2 + 2) * (3 + 4)`

#### Advanced Operations
- `calc_factorial(n)`: Calculate the factorial of n
- `calc_fibonacci(n)`: Calculate the nth Fibonacci number
- `stats(numbers)`: Calculate statistical measures for a list of numbers
- `quadratic(a, b, c)`: Solve a quadratic equation of the form ax² + bx + c = 0
- `angle_convert(angle, from_unit, to_unit)`: Convert an angle between different units

## Example

```python
# Client code example
from mcp.client import Client

# Connect to the calculator MCP server
client = Client(transport="stdio", command=["python", "calculator_mcp.py"])

# Basic operations
result = client.add(5, 3)  # Returns 8
result = client.calculate_expression("2 * (3 + 4)")  # Returns 14

# Advanced operations
result = client.calc_factorial(5)  # Returns 120
result = client.quadratic(1, -3, 2)  # Solves x² - 3x + 2 = 0
```

For a complete example, see the `example_client.py` file.

## Testing

Run the test suite to verify the functionality:

```bash
python test_calculator.py
```

To test the expression evaluator specifically:

```bash
python test_expression_evaluator.py
```

The test suite verifies all mathematical operations and error handling.

## Project Structure

- `calculator_mcp.py`: Main MCP server implementation
- `advanced_math.py`: Module containing advanced mathematical functions
- `example_client.py`: Example client demonstrating how to use the server
- `test_calculator.py`: Test suite for verifying functionality
- `test_expression_evaluator.py`: Test suite for the expression evaluator
- `run_server.py`: Script for running the server as a service
- `requirements.txt`: Python dependencies

## Extending

To add more mathematical functions:

1. Add the implementation to `advanced_math.py`
2. Create a new tool method in `calculator_mcp.py` that wraps the function
3. Update the documentation and examples as needed

## License

See the [LICENSE](LICENSE) file for details.