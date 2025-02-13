from compiler.tokenizer import Token
import compiler.ast as ast

def parse(tokens: list[Token]) -> ast.Expression:
    # This keeps track of which token we're looking at.
    pos = 0

    # 'peek()' returns the token at 'pos',
    # or a special 'end' token if we're past the end of the token list
    def peek() -> Token:
        if len(tokens) == 0:
            raise Exception(f'input was empty')
        if pos < len(tokens):
            return tokens[pos]
        else:
            return Token(
                loc=tokens[-1].loc,
                type="end",
                text="",
            )

    # 'consume(expected)' returns the token at 'pos', moves 'pos' forward
    def consume(expected: str | list[str] | None = None) -> Token:
        token = peek()
        if isinstance(expected, str) and token.text != expected:
            raise Exception(f'{token.loc}: expected "{expected}"')
        if isinstance(expected, list) and token.text not in expected:
            comma_separated = ", ".join([f'"{e}"' for e in expected])
            raise Exception(f'{token.loc}: expected one of: {comma_separated}')
        nonlocal pos
        pos += 1
        return token

    # the parsing function for integer literals.
    def parse_int_literal() -> ast.Literal:
        if peek().type != 'int_literal':
            raise Exception(f'{peek().loc}: expected an integer literal')
        token = consume()
        return ast.Literal(int(token.text))

    # the parsing function for identifiers.
    def parse_identifier() -> ast.Identifier:
        if peek().type != 'identifier':
            raise Exception(f'{peek().loc}: expected an identifier')
        token = consume()
        if peek().text == "(":
            return parse_function_call(ast.Identifier(token.text))
        return ast.Identifier(token.text)
    
    # parsing for function calls
    def parse_function_call(function_name: str) -> ast.FunctionCall:
        args = []
        consume('(')
        if peek().text == ")":
            consume(")")
            return ast.FunctionCall(function_name, args)
        while True:
            args.append(parse_expression())
            if peek().text == ")":
                break
            if peek().text == ",":
                consume(",")
        consume(')')
        return ast.FunctionCall(function_name, args)
    
    # the parsing function
    def parse_factor() -> ast.Expression:
      if peek().text == "(":
          return parse_parenthesized()
      elif peek().text in ["not", "-"]:
          return parse_unary_ops()
      elif peek().text == "if":
          return parse_if_expression()
      elif peek().type == 'int_literal':
          return parse_int_literal()
      elif peek().type == 'identifier':
          return parse_identifier()
      else:
          raise Exception(f'{peek().loc}: expected "(", "if", an integer literal or an identifier')

    # parsing function for unary operators - and not
    def parse_unary_ops() -> ast.Expression:
        while peek().text in ['-', 'not']:
            operator_token = consume()
            operator = operator_token.text
            operand = parse_factor()
        return ast.UnaryOp(operator, operand)
    
    # parsing for an assignment "="
    def parse_assignment():
        left: ast.Expression = parse_left_binary_operators()
        if peek().text == "=":
            consume("=")
            right = parse_assignment()
            return ast.BinaryOp(left, "=", right)
        return left
    
    # parsing function for left associative binary operators
    def parse_left_binary_operators() -> ast.Expression:
        left_associative_binary_operators = {op for l in [
            ['or'],
            ['and'],
            ['==', '!='],
            ['<', '<=', '>', '>='],
            ['+', '-'],
            ['*', '/', '%'],
        ] for op in l}

        left: ast.Expression = parse_term()
        while peek().text in left_associative_binary_operators:
            operator_token = consume()
            operator = operator_token.text
            right = parse_term()
            left = ast.BinaryOp(
                left,
                operator,
                right
            )
        return left
    
    # the parsing function for parenthesis
    def parse_parenthesized() -> ast.Expression:
      consume('(')
      # Recursively call the top level parsing function
      # to parse whatever is inside the parentheses.
      expr = parse_expression()
      consume(')')
      return expr
    
    # the parsing function for "+ and -" expressions
    def parse_expression() -> ast.Expression:
        left: ast.Expression = parse_left_binary_operators()
        while peek().text in ['+', '-']:
            operator_token = consume()
            operator = operator_token.text
            right = parse_left_binary_operators()
            left = ast.BinaryOp(
                left,
                operator,
                right
            )
        return left

    # the parsing function for "* and /" expressions
    def parse_term() -> ast.Expression:
        left: ast.Expression = parse_factor()
        while peek().text in ['*', '/', '%']:
            operator_token = consume()
            operator = operator_token.text
            right = parse_factor()
            left = ast.BinaryOp(
                left,
                operator,
                right
            )
        return left
    
    # parsing for if expressions
    def parse_if_expression() -> ast.Expression:
        consume("if")
        cond = parse_expression()
        consume("then")
        then_clause = parse_expression()
        if peek().text == "else":
            consume("else")
            else_clause = parse_expression()
        else:
            else_clause = None
        return ast.IfExpression(cond, then_clause, else_clause)
    
    # parsing for while expressions
    def parse_while_expression() -> ast.Expression:
        if peek().text == "while":
            consume("while")
            cond = parse_expression()
            body = parse_assignment()
            return ast.WhileExpression(cond, body)
        return parse_assignment()   # if not while, check right associative =
    
    # start parsing
    def start_parsing() -> ast.Expression:
        return parse_while_expression() # starts with while
    
    result = start_parsing()

    # Make sure the entire input is always parsed. Don’t allow garbage at the end of the input.
    if peek().type != 'end':
        raise Exception(f'{peek().loc}: unexpected token "{peek().text}"')

    return result