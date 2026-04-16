from nodes import *

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def eat(self, expected):
        if self.current() != expected:
            raise ValueError(f"Expected {expected}, got {self.current()}")
        self.pos += 1

    def parse(self):
        expr = self.parse_or()
        if self.current() is not None:
            raise ValueError(f"Unexpected token: {self.current()}")
        return expr

    def parse_or(self):
        left = self.parse_and()
        while self.current() == '+':
            self.eat('+')
            right = self.parse_and()
            left = Or(left, right)
        return left

    def parse_and(self):
        left = self.parse_not()
        while self.current() == '*':
            self.eat('*')
            right = self.parse_not()
            left = And(left, right)
        return left

    def parse_not(self):
        if self.current() == '!':
            self.eat('!')
            return Not(self.parse_not())
        return self.parse_primary()

    def parse_primary(self):
        tok = self.current()

        if tok == '(':
            self.eat('(')
            expr = self.parse_or()
            self.eat(')')
            return expr

        if tok in ('0', '1'):
            self.eat(tok)
            return Const(int(tok))

        if tok and tok.isalpha():
            self.eat(tok)
            return Var(tok)

        raise ValueError(f"Unexpected token: {tok}")

    def printTree(self, node, indent=0):
        prefix = ' ' * indent
        if isinstance(node, Var):
            print(f"{prefix}{node.name}")
        elif isinstance(node, Const):
            print(f"{prefix}{node.value}")
        elif isinstance(node, Not):
            print(f"{prefix}NOT")
            self.printTree(node.child, indent + 2)
        elif isinstance(node, And):
            print(f"{prefix}AND")
            self.printTree(node.left, indent + 2)
            self.printTree(node.right, indent + 2)
        elif isinstance(node, Or):
            print(f"{prefix}OR")
            self.printTree(node.left, indent + 2)
            self.printTree(node.right, indent + 2)