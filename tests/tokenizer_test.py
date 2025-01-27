from compiler.tokenizer import Token, tokenize, L

def test_tokenizer_basics() -> None:
    assert tokenize("   \n    hi   (hello)\n") == [
        Token(loc=L, type="identifier", text="hi"),
        Token(loc=L, type="punctuation", text="("),
        Token(loc=L, type="identifier", text="hello"),
        Token(loc=L, type="punctuation", text=")")
    ]

    assert tokenize("Hello {name}, compiler;project ") == [
        Token(loc=L, type="identifier", text="Hello"),
        Token(loc=L, type="punctuation", text="{"),
        Token(loc=L, type="identifier", text="name"),
        Token(loc=L, type="punctuation", text="}"),
        Token(loc=L, type="punctuation", text=","),
        Token(loc=L, type="identifier", text="compiler"),
        Token(loc=L, type="punctuation", text=";"),
        Token(loc=L, type="identifier", text="project"),
    ]

def test_tokenizer_skips_comments() -> None:
    assert tokenize("hello // testing testing \n //another comment \
                    # this is also a comment \
                    #and this") == [
        Token(loc=L, type="identifier", text="hello"),
    ]

def test_tokenizer_identifiers() -> None:
    assert tokenize("if  3\nwhile") == [
        Token(loc=L, type="identifier", text="if"),
        Token(loc=L, type="int_literal", text="3"),
        Token(loc=L, type="identifier", text="while")
    ]

def test_tokenizer_int_operators() -> None:
    assert tokenize("3-2") == [
        Token(loc=L, type="int_literal", text="3"),
        Token(loc=L, type="operator", text="-"),
        Token(loc=L, type="int_literal", text="2")
    ]

    assert tokenize("3 + -5") == [
        Token(loc=L, type="int_literal", text="3"),
        Token(loc=L, type="operator", text="+"),
        Token(loc=L, type="operator", text="-"),
        Token(loc=L, type="int_literal", text="5")
    ]

    assert tokenize("2*(4/2)=4==4 !=2 < 3 <= 3 > 2 >= 2") == [
        Token(loc=L, type="int_literal", text="2"),
        Token(loc=L, type="operator", text="*"),
        Token(loc=L, type="punctuation", text="("),
        Token(loc=L, type="int_literal", text="4"),
        Token(loc=L, type="operator", text="/"),
        Token(loc=L, type="int_literal", text="2"),
        Token(loc=L, type="punctuation", text=")"),
        Token(loc=L, type="operator", text="="),
        Token(loc=L, type="int_literal", text="4"),
        Token(loc=L, type="operator", text="=="),
        Token(loc=L, type="int_literal", text="4"),
        Token(loc=L, type="operator", text="!="),
        Token(loc=L, type="int_literal", text="2"),
        Token(loc=L, type="operator", text="<"),
        Token(loc=L, type="int_literal", text="3"),
        Token(loc=L, type="operator", text="<="),
        Token(loc=L, type="int_literal", text="3"),
        Token(loc=L, type="operator", text=">"),
        Token(loc=L, type="int_literal", text="2"),
        Token(loc=L, type="operator", text=">="),
        Token(loc=L, type="int_literal", text="2")
    ]