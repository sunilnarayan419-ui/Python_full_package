"""Demonstrations of the built-in eval() function, with explicit security treatment.

CRITICAL SECURITY NOTE:
eval() executes arbitrary Python expressions. It must never be called on
untrusted or user-supplied input. This module never passes external/user
input directly into eval(). The Industry-level implementation deliberately
avoids eval() entirely in favor of a safe, explicit expression evaluator.
"""

import ast
import operator


class UniversityEval:
    """Demonstrate eval() only on fixed, trusted, developer-authored expressions."""

    def __init__(self, trusted_expression: str) -> None:
        # trusted_expression is authored by the developer, never by external input.
        self.trusted_expression = trusted_expression

    def evaluate_trusted_expression(self) -> float:
        """Evaluate a hard-coded, trusted arithmetic expression.

        This is safe only because the expression is a fixed string written
        by the developer, not data received from a user or external source.
        """
        return eval(self.trusted_expression, {"__builtins__": {}}, {})

    @staticmethod
    def run() -> None:
        # Example: converting a concentration formula defined by the developer.
        processor = UniversityEval(trusted_expression="12.5 * 2 + 3")
        print(f"Trusted expression result: {processor.evaluate_trusted_expression()}")


class InterviewEval:
    """Demonstrate why eval() on arbitrary input is dangerous, and a safer design.

    This class intentionally does NOT evaluate untrusted input with eval().
    Instead it shows the risk conceptually and demonstrates a restricted,
    sandboxed evaluation using a limited namespace as an interview-style
    discussion point, while still recommending avoiding eval() entirely
    for real user input (see IndustryEval for the safe production approach).
    """

    @staticmethod
    def explain_risk() -> str:
        return (
            "eval(user_input) can execute arbitrary code, access the "
            "filesystem, or exfiltrate data. Never call eval() directly on "
            "untrusted input, even with a restricted __builtins__ dict, "
            "since sandboxing eval() is notoriously difficult to make safe."
        )

    @staticmethod
    def restricted_namespace_demo(trusted_expression: str) -> float:
        """Illustrate a restricted namespace; still only used on trusted input."""
        allowed_names: dict[str, object] = {"__builtins__": {}}
        return eval(trusted_expression, allowed_names, {})

    @staticmethod
    def run() -> None:
        print(InterviewEval.explain_risk())

        case_one = "3 + 4 * 2"
        case_two = "10 / 2"
        print(f"Restricted eval on '{case_one}': {InterviewEval.restricted_namespace_demo(case_one)}")
        print(f"Restricted eval on '{case_two}': {InterviewEval.restricted_namespace_demo(case_two)}")


class IndustryEval:
    """Production-safe alternative to eval(): an explicit, allow-listed evaluator.

    Rather than using eval() on user-supplied formulas (e.g. lab technicians
    entering calculation formulas), this class parses expressions with the
    `ast` module and only permits a small, explicit set of safe operations.
    Anything outside the allow-list is rejected before any computation runs.
    """

    _ALLOWED_OPERATORS: dict[type, object] = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.USub: operator.neg,
    }

    def evaluate_safe_expression(self, expression: str) -> float:
        """Safely evaluate a restricted arithmetic expression from user input.

        Only numeric literals and +, -, *, /, and unary minus are permitted.
        No function calls, attribute access, or names are allowed.
        """
        parsed_expression = ast.parse(expression, mode="eval").body
        return self._evaluate_node(parsed_expression)

    def _evaluate_node(self, node: ast.AST) -> float:
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value

        if isinstance(node, ast.BinOp) and type(node.op) in self._ALLOWED_OPERATORS:
            left_value = self._evaluate_node(node.left)
            right_value = self._evaluate_node(node.right)
            return self._ALLOWED_OPERATORS[type(node.op)](left_value, right_value)

        if isinstance(node, ast.UnaryOp) and type(node.op) in self._ALLOWED_OPERATORS:
            operand_value = self._evaluate_node(node.operand)
            return self._ALLOWED_OPERATORS[type(node.op)](operand_value)

        raise ValueError(f"Disallowed expression element: {type(node).__name__}")

    @staticmethod
    def run() -> None:
        evaluator = IndustryEval()

        safe_inputs = ["12.5 * 2 + 3", "(4 - 1) / 2", "-5 + 10"]
        for expression in safe_inputs:
            result = evaluator.evaluate_safe_expression(expression)
            print(f"Safe expression '{expression}' -> {result}")

        dangerous_input = "__import__('os').system('echo unsafe')"
        try:
            evaluator.evaluate_safe_expression(dangerous_input)
        except (ValueError, SyntaxError) as error:
            print(f"Rejected dangerous input: {error}")


if __name__ == "__main__":
    UniversityEval.run()
    InterviewEval.run()
    IndustryEval.run()
