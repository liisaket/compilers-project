import pytest
from compiler import ast
from compiler.parser import parse
from compiler.tokenizer import tokenize


def test_parser_basics() -> None:
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

def test_if_clauses() -> None:
  assert parse(tokenize("if 1 then 2")) == ast.IfExpression(
    cond=ast.Literal(1),
    then_clause=ast.Literal(2),
    else_clause=None
  )
  
  assert parse(tokenize("if a then b + c")) == ast.IfExpression(
    cond=ast.Identifier("a"),
    then_clause=ast.BinaryOp(ast.Identifier("b"), "+", ast.Identifier("c")),
    else_clause=None
  )

  assert parse(tokenize("if a then b + c else x * y")) == ast.IfExpression(
    cond=ast.Identifier("a"),
    then_clause=ast.BinaryOp(ast.Identifier("b"), "+", ast.Identifier("c")),
    else_clause=ast.BinaryOp(
      left=ast.Identifier("x"),
      op="*",
      right=ast.Identifier("y")
    ),
  )

  assert parse(tokenize("1 + if true then 2 else 3")) == ast.BinaryOp(
    left=ast.Literal(1),
    op="+",
    right=ast.IfExpression(
      cond=ast.Identifier("true"),  # booleans not yet implemented
      then_clause=ast.Literal(2),
      else_clause=ast.Literal(3)
    )
  )

def test_nested_if_clauses() -> None:
  assert parse(tokenize("if true then 2 else if false then 3 else 4")) == ast.IfExpression(
    cond=ast.Identifier("true"),
    then_clause=ast.Literal(2),
    else_clause=ast.IfExpression(
      cond=ast.Identifier("false"),
      then_clause=ast.Literal(3),
      else_clause=ast.Literal(4)
    )
  )
  
  assert parse(tokenize("if 2 + 2 then if 1 + 3 then 4 else 5 else 6")) == ast.IfExpression(
    cond=ast.BinaryOp(
      left=ast.Literal(2),
      op="+",
      right=ast.Literal(2),
    ),
    then_clause=ast.IfExpression(
      cond=ast.BinaryOp(
        left=ast.Literal(1),
        op="+",
        right=ast.Literal(3)),
      then_clause=ast.Literal(4),
      else_clause=ast.Literal(5)
    ),
    else_clause=ast.Literal(6)
    )

def test_function_call() -> None:
  assert parse(tokenize("my_function(a)")) == ast.FunctionCall(
    name=ast.Identifier("my_function"),
    arguments=[ast.Identifier("a")]
  )

  assert parse(tokenize("my_function(a, b)")) == ast.FunctionCall(
    name=ast.Identifier("my_function"),
    arguments=[ast.Identifier("a"), ast.Identifier("b")]
  )

  assert parse(tokenize("f(x, y + z)")) == ast.FunctionCall(
    name=ast.Identifier("f"),
    arguments=[ast.Identifier("x"), ast.BinaryOp(
      left=ast.Identifier("y"),
      op="+",
      right=ast.Identifier("z")
    )])
  
  assert parse(tokenize("f(x + y, g(z))")) == ast.FunctionCall(
    name=ast.Identifier("f"),
    arguments=[
      ast.BinaryOp(ast.Identifier("x"), "+", ast.Identifier("y")),
      ast.FunctionCall(ast.Identifier("g"), [ast.Identifier("z")])
    ])
  
  assert parse(tokenize("f(1, 2 * 3)")) == ast.FunctionCall(
    name=ast.Identifier("f"),
    arguments=[ast.Literal(1), ast.BinaryOp(
      left=ast.Literal(2),
      op="*",
      right=ast.Literal(3)
    )])
  
  # empty, no arguments
  assert parse(tokenize("my_function()")) == ast.FunctionCall(
    name=ast.Identifier("my_function"),
    arguments=[]
  )

def test_more_operators() -> None:
  assert parse(tokenize("1 == 1")) == ast.BinaryOp(
    left=ast.Literal(1),
    op="==",
    right=ast.Literal(1)
  )
  assert parse(tokenize("2 > 1")) == ast.BinaryOp(
    left=ast.Literal(2),
    op=">",
    right=ast.Literal(1)
  )
  assert parse(tokenize("1 < 2")) == ast.BinaryOp(
    left=ast.Literal(1),
    op="<",
    right=ast.Literal(2)
  )
  assert parse(tokenize("1 != 2")) == ast.BinaryOp(
    left=ast.Literal(1),
    op="!=",
    right=ast.Literal(2)
  )
  assert parse(tokenize("1 and 2")) == ast.BinaryOp(
    left=ast.Literal(1),
    op="and",
    right=ast.Literal(2)
  )
  assert parse(tokenize("1 or 2")) == ast.BinaryOp(
    left=ast.Literal(1),
    op="or",
    right=ast.Literal(2)
  )
  assert parse(tokenize("1 >= 1 <= 1")) == ast.BinaryOp(
    left=ast.BinaryOp(
      left=ast.Literal(1),
      op=">=",
      right=ast.Literal(1)
    ),
    op="<=",
    right=ast.Literal(1)
  )
  assert parse(tokenize("1%1")) == ast.BinaryOp(
    left=ast.Literal(1),
    op="%",
    right=ast.Literal(1)
  )

def test_unary_not() -> None:
  assert parse(tokenize("not x")) == ast.UnaryOp(
    op="not",
    value=ast.Identifier("x")
  )
  assert parse(tokenize("not 1")) == ast.UnaryOp(
    op="not",
    value=ast.Literal(1)
  )
  assert parse(tokenize("not not x")) == ast.UnaryOp(
    op="not",
    value=ast.UnaryOp("not", ast.Identifier("x"))
  )
  assert parse(tokenize("not (x and y)")) == ast.UnaryOp(
    op="not",
    value=ast.BinaryOp(
      left=ast.Identifier("x"),
      op="and",
      right=ast.Identifier("y")
  ))

def test_unary_minus() -> None:
  assert parse(tokenize("-x")) == ast.UnaryOp(
    op="-",
    value=ast.Identifier("x")
  )
  assert parse(tokenize("--x")) == ast.UnaryOp(
    op="-",
    value=ast.UnaryOp("-", ast.Identifier("x"))
  )
  assert parse(tokenize("-1 + 2")) == ast.BinaryOp(
    left=ast.UnaryOp("-", ast.Literal(1)),
    op="+",
    right=ast.Literal(2)
  )
  assert parse(tokenize("-(1 + 2)")) == ast.UnaryOp(
    op="-",
    value=ast.BinaryOp(
      left=ast.Literal(1),
      op="+",
      right=ast.Literal(2)
  ))

def test_right_associative_operators() -> None:
  assert parse(tokenize("a = b")) == ast.BinaryOp(
    left=ast.Identifier("a"),
    op="=",
    right=ast.Identifier("b")
  )

  assert parse(tokenize("a = b = c")) == ast.BinaryOp(
    left=ast.Identifier("a"),
    op="=",
    right=ast.BinaryOp(
      left=ast.Identifier("b"),
      op="=",
      right=ast.Identifier("c")
    )
  )

def test_while_clauses() -> None:
  assert parse(tokenize("while true 1 + 1")) == ast.WhileExpression(
    cond=ast.Identifier("true"),
    body=ast.BinaryOp(ast.Literal(1), "+", ast.Literal(1))
  )

  assert parse(tokenize("while (x < 10) x = x + 1")) == ast.WhileExpression(
    cond=ast.BinaryOp(ast.Identifier("x"), "<", ast.Literal(10)),
    body=ast.BinaryOp(
      ast.Identifier("x"),
      "=",
      ast.BinaryOp(ast.Identifier("x"), "+", ast.Literal(1))
    )
  )