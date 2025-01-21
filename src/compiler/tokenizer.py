from dataclasses import dataclass
from typing import Literal
import re

TokenType = Literal["int_literal", "identifier", "operator", "punctuation", "end"]

@dataclass(frozen=True)
class Location:
  file: str
  line: str
  column: str

@dataclass(frozen=True)
class Token:
  type: TokenType
  text: str
  #loc: Location


def tokenize(source_code: str) -> list[Token]:
  tokens = {
    re.compile(r"[0-9]+"): "int_literal",
    re.compile(r"[a-zA-Z_][a-zA-Z0-9_]*"): "identifier",
    re.compile(r"==|!=|<=|>=|=|<|>|\+|\-|\*|\/"): "operator",
    re.compile(r"[(){},;]"): "punctuation",
    re.compile(r"\s+"): "whitespace",
    re.compile(r"#|//.*"): "comment"
  }

  position = 0
  result: list[Token] = []

  while position < len(source_code):
    for k, v in tokens.items():
      match = k.match(source_code, position)
      if match != None:
        if v not in ["whitespace", "comment"]:
          result.append(Token(
          type=tokens[k],
          text=source_code[position:match.end()]
        ))
        position = match.end()

    #raise Exception(f"Tokenization failed near {source_code[position:match.end(): (position +10)]}")

  return result