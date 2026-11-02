
import ast
import operator
import re
from dataclasses import dataclass, field


BINARY_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

COMPARISON_OPERATORS = {
    ast.Eq: operator.eq,
    ast.NotEq: operator.ne,
    ast.Lt: operator.lt,
    ast.LtE: operator.le,
    ast.Gt: operator.gt,
    ast.GtE: operator.ge,
}

MAX_POWER = 100


@dataclass
class OptimizationResult:
    code: str
    logs: list = field(default_factory=list)
    folded_count: int = 0
    changed_lines: int = 0
    original_lines: int = 0


def is_number(node):
    return (
        isinstance(node, ast.Constant)
        and type(node.value) in (int, float)
    )


def fmt(value):
    if isinstance(value, bool):
        return "1" if value else "0"
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return str(value)


def safe_number(value):
    if type(value) not in (int, float):
        return False
    if isinstance(value, float):
        return value == value and abs(value) != float("inf")
    return True


def fold_node(node, logs):
    """Recursively fold constant subexpressions in an AST."""

    if isinstance(node, ast.BinOp):
        node.left = fold_node(node.left, logs)
        node.right = fold_node(node.right, logs)

        if (
            is_number(node.left)
            and is_number(node.right)
            and type(node.op) in BINARY_OPERATORS
        ):
            left, right = node.left.value, node.right.value

            if isinstance(node.op, ast.Pow):
                if abs(right) > MAX_POWER:
                    return node
                if abs(left) > 1 and right > 50:
                    return node

            try:
                value = BINARY_OPERATORS[type(node.op)](
                    left, right
                )
                if not safe_number(value):
                    return node

                before = ast.unparse(node)
                logs.append(
                    f"Constant folding: {before} -> {fmt(value)}"
                )
                return ast.Constant(value=value)

            except (ArithmeticError, OverflowError, ValueError):
                logs.append(
                    f"Skipped invalid arithmetic: {ast.unparse(node)}"
                )

        return node

    if isinstance(node, ast.UnaryOp):
        node.operand = fold_node(node.operand, logs)

        if is_number(node.operand):
            value = node.operand.value

            if isinstance(node.op, ast.USub):
                result = -value
            elif isinstance(node.op, ast.UAdd):
                result = value
            else:
                return node

            logs.append(
                f"Constant folding: {ast.unparse(node)} -> {fmt(result)}"
            )
            return ast.Constant(value=result)

        return node

    if isinstance(node, ast.Compare):
        node.left = fold_node(node.left, logs)
        node.comparators = [
            fold_node(item, logs) for item in node.comparators
        ]

        if (
            len(node.ops) == 1
            and is_number(node.left)
            and is_number(node.comparators[0])
            and type(node.ops[0]) in COMPARISON_OPERATORS
        ):
            try:
                result = COMPARISON_OPERATORS[type(node.ops[0])](
                    node.left.value, node.comparators[0].value
                )
                before = ast.unparse(node)
                logs.append(
                    f"Constant comparison: {before} -> {fmt(result)}"
                )
                return ast.Constant(value=int(result))
            except (ArithmeticError, TypeError, ValueError):
                return node

        return node

    if isinstance(node, ast.BoolOp):
        node.values = [fold_node(item, logs) for item in node.values]
        return node

    return node


ALLOWED_NODES = (
    ast.Expression, ast.Constant, ast.Name, ast.Load,
    ast.BinOp, ast.UnaryOp, ast.Compare, ast.BoolOp,
    ast.Add, ast.Sub, ast.Mult, ast.Div, ast.FloorDiv,
    ast.Mod, ast.Pow, ast.UAdd, ast.USub,
    ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE,
    ast.And, ast.Or,
)


def optimize_expression(expression, logs):
    """Parse a restricted expression without executing user code."""

    expression = expression.strip()
    if not expression:
        return expression

    try:
        tree = ast.parse(expression, mode="eval")
    except (SyntaxError, ValueError):
        return expression

    if any(
        not isinstance(node, ALLOWED_NODES)
        for node in ast.walk(tree)
    ):
        logs.append(f"Unsupported expression left unchanged: {expression}")
        return expression

    tree.body = fold_node(tree.body, logs)
    return ast.unparse(tree.body)


def optimize_source(source):
    """
    Optimize expressions in simple C-style declarations, assignments,
    return statements, and if/while conditions.

    This is a subset optimizer, not a complete C compiler.
    """

    output = []
    logs = []
    changed_lines = 0
    folded_count = 0
    source_lines = source.splitlines()

    # Handles simple declarations/assignments and return expressions.
    assignment_pattern = re.compile(
        r"^(\s*(?:(?:int|float|double|long|short|char|bool)\s+)?"
        r"[A-Za-z_]\w*\s*=\s*)(.*?)"
        r"(;\s*(?://.*)?)$"
    )
    return_pattern = re.compile(r"^(\s*return\s+)(.*?)(;\s*)$")
    condition_pattern = re.compile(
        r"^(\s*(?:if|while)\s*\()(.*?)(\)\s*\{?\s*)$"
    )

    for line_number, line in enumerate(source_lines, start=1):
        logs_for_line = []
        new_line = line

        match = assignment_pattern.match(line)
        if match:
            prefix, expression, suffix = match.groups()
            optimized = optimize_expression(expression, logs_for_line)
            new_line = prefix + optimized + suffix

        else:
            match = return_pattern.match(line)
            if match:
                prefix, expression, suffix = match.groups()
                optimized = optimize_expression(
                    expression, logs_for_line
                )
                new_line = prefix + optimized + suffix

            else:
                match = condition_pattern.match(line)
                if match:
                    prefix, expression, suffix = match.groups()
                    optimized = optimize_expression(
                        expression, logs_for_line
                    )
                    new_line = prefix + optimized + suffix

        if new_line != line:
            changed_lines += 1

        if logs_for_line:
            logs.append(f"Line {line_number}:")
            logs.extend(f"  {item}" for item in logs_for_line)
            folded_count += sum(
                1 for item in logs_for_line
                if item.startswith(
                    ("Constant folding:", "Constant comparison:")
                )
            )

        output.append(new_line)

    if not logs:
        logs.append(
            "No constant expressions were folded in the supported "
            "statements."
        )

    return OptimizationResult(
        code="\n".join(output),
        logs=logs,
        folded_count=folded_count,
        changed_lines=changed_lines,
        original_lines=len(source_lines),
    )
