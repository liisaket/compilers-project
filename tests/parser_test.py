import pytest
from compiler import ast
from compiler.parser import parse
from compiler.tokenizer import tokenize


def test_parser() -> None:
  assert parse(tokenize("1 + 2")) == ast.BinaryOp(
    left=ast.Literal(1),
    op="+",
    right=ast.Literal(2)
  )

  assert parse(tokenize("1 + 2 - 3")) == ast.BinaryOp(
    left=ast.BinaryOp(
      left=ast.Literal(1),
      op="+",
      right=ast.Literal(2),
    ),
    op="-",
    right=ast.Literal(3)
  )

  assert parse(tokenize("1 + 2 * 3")) == ast.BinaryOp(
    left=ast.Literal(1),
    op="+",
    right=ast.BinaryOp(
      left=ast.Literal(2),
      op="*",
      right=ast.Literal(3),
    ),
  )

  assert parse(tokenize("1 * 5 + 2 * 3")) == ast.BinaryOp(
    left=ast.BinaryOp(
      left=ast.Literal(1),
      op="*",
      right=ast.Literal(5)
    ),
    op="+",
    right=ast.BinaryOp(
      left=ast.Literal(2),
      op="*",
      right=ast.Literal(3),
    ),
  )

  assert parse(tokenize("1")) == ast.Literal(1)

  assert parse(tokenize("1 * (2 + 3)")) == ast.BinaryOp(
    left=ast.Literal(1),
    op="*",
    right=ast.BinaryOp(
      left=ast.Literal(2),
      op="+",
      right=ast.Literal(3)
    )
  )

  assert parse(tokenize("(2 + 3) + 4")) == ast.BinaryOp(
    left=ast.BinaryOp(
      left=ast.Literal(2),
      op="+",
      right=ast.Literal(3)
    ),
    op="+",
    right=ast.Literal(4),
  )

  assert parse(tokenize("1 * (2 + 3) / 4")) == ast.BinaryOp(
    left=ast.BinaryOp(
      left=ast.Literal(1),
      op="*",
      right=ast.BinaryOp(
        left=ast.Literal(2),
        op="+",
        right=ast.Literal(3)
    )),
    op="/",
    right=ast.Literal(4),
  )

def test_bad_input_fails() -> None:
  with pytest.raises(Exception, match='unexpected token "c"'):
    parse(tokenize("a + b c"))

def test_empty_input_fails() -> None:
  with pytest.raises(Exception, match='input was empty'):
    parse(tokenize(""))

