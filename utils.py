from syntax import SyntaxTree
import numpy as np
import random
import time

def initialize(terminals, primitive_symbol):
    #random.seed(time.time())
    type = random.randint(1,4)
    if type == 1:
        type = 'constante'
        value = float(random.randint(0,100))
        symbol = str(value)
    elif type == 2:
        type = 'terminal'
        symbol = terminals[random.randint(0, len(terminals)-1)]
        value = None
    else:
        type = 'primitiva'
        symbol = primitive_symbol[random.randint(0, len(primitive_symbol)-1)]
        value = None

    t = SyntaxTree(type, symbol)
    if type == 'constante':
        t.value = value
        return t
    elif type == 'terminal':
        return t
    else:
        if(symbol=='+' or symbol=='-' or symbol=='*' or symbol=='/' or symbol=='^'):
            l = initialize(terminals, primitive_symbol)
            l.up = t
            r = initialize(terminals, primitive_symbol)
            r.up = t
            t.left = l
            t.right = r
        else: #Primitivas que utilizam apenas 1 valor
            l = initialize(terminals, primitive_symbol)
            l.up = t
            t.left = l
    return t
