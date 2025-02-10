from dataclasses import dataclass

@dataclass
class Expression:
    """Base class for AST nodes representing expressions."""

@dataclass
class Literal(Expression):
    value: int | bool

@dataclass
class Identifier(Expression):
    name: str

@dataclass
class BinaryOp(Expression):
    """AST node for a binary operation like `A + B`"""
    left: Expression
    op: str
    right: Expression

@dataclass
class IfExpression(Expression):
    cond: Expression
    then_clause: Expression
    else_clause: Expression | None

@dataclass
class WhileExpression(Expression):
    cond: Expression
    body: Expression

@dataclass
class FunctionCall(Expression):
    name: Identifier
    arguments: list[Expression]

@dataclass
class UnaryOp(Expression):
    op: str
    value: Expression