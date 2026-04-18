"""Expression tokenizer, parser, tree printer, and evaluator for Q2."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Token:
    kind: str
    value: str


@dataclass(frozen=True)
class NumberNode:
    value: int


@dataclass(frozen=True)
class UnaryNode:
    op: str
    operand: "ASTNode"


@dataclass(frozen=True)
class BinaryNode:
    op: str
    left: "ASTNode"
    right: "ASTNode"


ASTNode = NumberNode | UnaryNode | BinaryNode


class Lexer:
    @staticmethod
    def tokenize(expression: str) -> list[Token]:
        tokens: list[Token] = []
        index = 0

        while index < len(expression):
            char = expression[index]

            if char.isspace():
                index += 1
                continue

            if char.isdigit():
                start = index
                while index < len(expression) and expression[index].isdigit():
                    index += 1
                tokens.append(Token("NUM", expression[start:index]))
                continue

            if char in "+-*/":
                tokens.append(Token("OP", char))
                index += 1
                continue

            if char == "(":
                tokens.append(Token("LPAREN", char))
                index += 1
                continue

            if char == ")":
                tokens.append(Token("RPAREN", char))
                index += 1
                continue

            raise ValueError(f"Invalid character: {char}")

        tokens.append(Token("END", ""))
        return tokens


class Parser:
    def __init__(self, tokens: list[Token]) -> None:
        self.tokens = tokens
        self.position = 0

    def _current(self) -> Token:
        return self.tokens[self.position]

    def _advance(self) -> Token:
        token = self._current()
        self.position += 1
        return token

    def parse(self) -> ASTNode:
        node = self._expression()
        if self._current().kind != "END":
            raise ValueError("Unexpected trailing tokens")
        return node

    def _expression(self) -> ASTNode:
        node = self._term()

        while self._current().kind == "OP" and self._current().value in {"+", "-"}:
            operator = self._advance().value
            right = self._term()
            node = BinaryNode(operator, node, right)

        return node

    def _term(self) -> ASTNode:
        node = self._factor()

        while self._current().kind == "OP" and self._current().value in {"*", "/"}:
            operator = self._advance().value
            right = self._factor()
            node = BinaryNode(operator, node, right)

        return node

    def _factor(self) -> ASTNode:
        token = self._current()

        if token.kind == "OP" and token.value == "-":
            self._advance()
            return UnaryNode("neg", self._factor())

        if token.kind == "NUM":
            self._advance()
            return NumberNode(int(token.value))

        if token.kind == "LPAREN":
            self._advance()
            node = self._expression()
            if self._current().kind != "RPAREN":
                raise ValueError("Missing closing parenthesis")
            self._advance()
            return node

        raise ValueError("Unexpected token")


class Evaluator:
    @staticmethod
    def evaluate(node: ASTNode) -> int | float:
        if isinstance(node, NumberNode):
            return node.value

        if isinstance(node, UnaryNode):
            operand = Evaluator.evaluate(node.operand)
            if node.op == "neg":
                return -operand
            raise ValueError("Unsupported unary operator")

        left = Evaluator.evaluate(node.left)
        right = Evaluator.evaluate(node.right)

        if node.op == "+":
            return left + right
        if node.op == "-":
            return left - right
        if node.op == "*":
            return left * right
        if node.op == "/":
            if right == 0:
                raise ZeroDivisionError("Division by zero")
            return left / right

        raise ValueError("Unsupported binary operator")


class Formatter:
    @staticmethod
    def token_list(tokens: list[Token]) -> str:
        formatted_tokens: list[str] = []
        for token in tokens:
            if token.kind == "END":
                formatted_tokens.append("[END]")
            else:
                formatted_tokens.append(f"[{token.kind}:{token.value}]")
        return " ".join(formatted_tokens)

    @staticmethod
    def tree(node: ASTNode) -> str:
        if isinstance(node, NumberNode):
            return str(node.value)

        if isinstance(node, UnaryNode):
            return f"({node.op} {Formatter.tree(node.operand)})"

        return f"({node.op} {Formatter.tree(node.left)} {Formatter.tree(node.right)})"

    @staticmethod
    def result(value: int | float) -> str:
        if isinstance(value, float) and value.is_integer():
            return str(int(value))
        return str(value)


class ExpressionProcessor:
    @staticmethod
    def process(expression: str) -> tuple[str, str, str]:
        try:
            tokens = Lexer.tokenize(expression)
            parser = Parser(tokens)
            ast = parser.parse()
        except ValueError:
            return "ERROR", "ERROR", "ERROR"

        tree_output = Formatter.tree(ast)
        token_output = Formatter.token_list(tokens)

        try:
            value = Evaluator.evaluate(ast)
            result_output = Formatter.result(value)
        except ZeroDivisionError:
            result_output = "ERROR"

        return tree_output, token_output, result_output


BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR / "sample_input.txt"
OUTPUT_FILE = BASE_DIR / "output.txt"


def read_expressions() -> list[str]:
    if not INPUT_FILE.exists():
        raise FileNotFoundError(f"Input file not found: {INPUT_FILE}")

    lines = INPUT_FILE.read_text(encoding="utf-8").splitlines()
    return [line.strip() for line in lines if line.strip()]


def format_output_block(expression: str) -> str:
    tree_output, token_output, result_output = ExpressionProcessor.process(expression)
    return (
        f"Input: {expression}\n"
        f"Tree: {tree_output}\n"
        f"Tokens: {token_output}\n"
        f"Result: {result_output}"
    )


def write_output(expressions: list[str]) -> None:
    blocks = [format_output_block(expression) for expression in expressions]
    OUTPUT_FILE.write_text("\n\n".join(blocks) + "\n", encoding="utf-8")


def main() -> None:
    expressions = read_expressions()
    write_output(expressions)


if __name__ == "__main__":
    main()
