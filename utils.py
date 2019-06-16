from syntax import SyntaxTree
import numpy as np
import random
import time

def initialize(terminals, primitive_symbol, up=None):
    #random.seed(time.time())
    type = random.randint(1,4)
    if type == 1:
        type = 'constante'
        value = np.float(random.randint(0,100))
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
        t.up = up
    elif type == 'terminal':
        t.up = up
    else:
        if(symbol=='+' or symbol=='-' or symbol=='*' or symbol=='/' or symbol=='^'):
            l = initialize(terminals, primitive_symbol, up=t)
            r = initialize(terminals, primitive_symbol, up=t)
            t.left = l
            t.right = r
            t.up = up
        else: #Primitivas que utilizam apenas 1 valor
            l = initialize(terminals, primitive_symbol, up=t)
            t.left = l
            t.up = up
    return t
