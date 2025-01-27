from dataclasses import dataclass
from typing import Literal
import re

TokenType = Literal["int_literal", "identifier", "operator", "punctuation", "end"]

L = object()

@dataclass(frozen=True)
class Location:
  file: str
  line: int
  column: int

  def __eq__(self, value):
    if value == L:
      return True
    return (self.file, self.line, self.column) == (value.file, value.line, value.column)
  
class TestLocation:
  def __eq__(self, value):
    pass

@dataclass(frozen=True)
class Token:
  type: TokenType
  text: str
  loc: Location

def tokenize(source_code: str) -> list[Token]:
  tokens = {
    re.compile(r"[0-9]+"): "int_literal",
    re.compile(r"[a-zA-Z_][a-zA-Z0-9_]*"): "identifier",
    re.compile(r"==|!=|<=|>=|=|<|>|\+|\-|\*|\/"): "operator",
    re.compile(r"[(){},;]"): "punctuation",
    re.compile(r"\s+"): "whitespace",
    re.compile(r"#|//.*"): "comment"
  }

  result: list[Token] = []
  position = 0

  while position < len(source_code):
    for k, v in tokens.items():
      match = k.match(source_code, position)
      if match != None:
        if v not in ["whitespace", "comment"]:
          line = source_code.count("\n", 0, match.start()) + 1
          last_newline = source_code.rfind("\n", 0, match.start())
          column = (match.start() - last_newline) if last_newline != -1 else (match.start() + 1)  
          result.append(Token(
          type=tokens[k],
          text=source_code[position:match.end()],
          loc=Location(__file__, line, column)
        ))
        position = match.end()

    #raise Exception(f"Tokenization failed near {source_code[position:match.end(): (position +10)]}")

  return result