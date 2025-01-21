from compiler.tokenizer import Token, tokenize

def test_tokenizer_basics() -> None:
    assert tokenize("   \n    hi   (hello)\n") == [
        Token(type="identifier", text="hi"),
        Token(type="punctuation", text="("),
        Token(type="identifier", text="hello"),
        Token(type="punctuation", text=")")
    ]

    assert tokenize("Hello {name}, compiler;project ") == [
        Token(type="identifier", text="Hello"),
        Token(type="punctuation", text="{"),
        Token(type="identifier", text="name"),
        Token(type="punctuation", text="}"),
        Token(type="punctuation", text=","),
        Token(type="identifier", text="compiler"),
        Token(type="punctuation", text=";"),
        Token(type="identifier", text="project"),
    ]


def test_tokenizer_skips_comments() -> None:
    assert tokenize("hello // testing testing \n //another comment \
                    # this is also a comment \
                    #and this") == [
        Token(type="identifier", text="hello"),
    ]

def test_tokenizer_identifiers() -> None:
    assert tokenize("if  3\nwhile") == [
        Token(type="identifier", text="if"),
        Token(type="int_literal", text="3"),
        Token(type="identifier", text="while")
    ]

def test_tokenizer_int_operators() -> None:
    assert tokenize("3-2") == [
        Token(type="int_literal", text="3"),
        Token(type="operator", text="-"),
        Token(type="int_literal", text="2")
    ]

    assert tokenize("3 + -5") == [
        Token(type="int_literal", text="3"),
        Token(type="operator", text="+"),
        Token(type="operator", text="-"),
        Token(type="int_literal", text="5")
    ]

    assert tokenize("2*(4/2)=4==4 !=2 < 3 <= 3 > 2 >= 2") == [
        Token(type="int_literal", text="2"),
        Token(type="operator", text="*"),
        Token(type="punctuation", text="("),
        Token(type="int_literal", text="4"),
        Token(type="operator", text="/"),
        Token(type="int_literal", text="2"),
        Token(type="punctuation", text=")"),
        Token(type="operator", text="="),
        Token(type="int_literal", text="4"),
        Token(type="operator", text="=="),
        Token(type="int_literal", text="4"),
        Token(type="operator", text="!="),
        Token(type="int_literal", text="2"),
        Token(type="operator", text="<"),
        Token(type="int_literal", text="3"),
        Token(type="operator", text="<="),
        Token(type="int_literal", text="3"),
        Token(type="operator", text=">"),
        Token(type="int_literal", text="2"),
        Token(type="operator", text=">="),
        Token(type="int_literal", text="2")
    ]