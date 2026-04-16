from parser import *
from myToken import *
from simplifierLogic import * 
from nodes import *

expr_str = "(A+0)*(A+1)"

print("Input:", expr_str)

tokens = token(expr_str)
print("Tokens:", tokens)

parser = Parser(tokens)
ast = parser.parse()

print("\nOriginal tree:")
parser.printTree(ast)

simplified = simplify_full(ast)

print("\nSimplified tree:")
parser.printTree(simplified)

print("\nOriginal:", to_string(ast))
print("Simplified:", to_string(simplified))