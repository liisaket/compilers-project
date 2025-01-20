from compiler.tokenizer import Token, tokenize

def test_tokenizer_basics() -> None:
    assert tokenize("   \n    hi   (hello)\n") == [
        Token(type="identifier", text="hi"),
        Token(type="parenthesis", text="("),
        Token(type="identifier", text="hello"),
        Token(type="parenthesis", text=")")
    ]

def test_tokenizer_identifiers() -> None:
    assert tokenize("if  3\nwhile") == [
        Token(type="identifier", text="if"),
        Token(type="int_literal", text="3"),
        Token(type="identifier", text="while")
    ]

def test_tokenizer_int_literals() -> None:
    assert tokenize("3-2") == [
        Token(type="int_literal", text="3"),
        Token(type="identifier", text="-"),
        Token(type="int_literal", text="2")
    ]