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
    re.compile(r"\s+"): "whitespace",
    re.compile(r"//.*|#.*"): "comment",
    re.compile(r"[0-9]+"): "int_literal",
    re.compile(r"[a-zA-Z_][a-zA-Z0-9_]*"): "identifier",
    re.compile(r"==|!=|<=|>=|=|<|>|\+|\-|\*|\/|%"): "operator",
    re.compile(r"[(){},;]"): "punctuation",
  }

  result: list[Token] = []
  source_len = len(source_code)
  position = 0

  while position < source_len:
    match_found = False   # tracks if match was found at current position
    for regex, token_type in tokens.items():
      match = regex.match(source_code, position)
      if match:
        match_found = True
        match_text = match.group(0)
        if token_type not in ["whitespace", "comment"]:
          line = source_code.count("\n", 0, match.start()) + 1
          last_newline = source_code.rfind("\n", 0, match.start())
          column = (match.start() - last_newline) if last_newline != -1 else (match.start() + 1)  
          result.append(Token(
          type=token_type,
          text=match_text,
          loc=Location(__file__, line, column)
        ))
        position = match.end()
        break

    if not match_found:
      raise Exception(f"Tokenization failed near: '{source_code[position:position + 10]}' at position {position}")

  return result