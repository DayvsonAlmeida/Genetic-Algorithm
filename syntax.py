import numpy as np

class SyntaxTree(object):
    def __init__(self, type, symbol):
        self.type = type        # Tipo de nó {terminal, primitiva, constante}
        self.symbol = symbol    # Símbolo que representa a primitiva ou terminal
        self.value = []         # Resultados da sub-árvore para cada entrada

        self.up = None          # Pai do nó
        self.left = None        # Filho esquerdo do nó
        self.right = None       # Filho direito do nó
        self.conversor = Conversor()

    def run(self, input):
        if self.type == 'constante':
            return np.array([self.value])
        elif self.type == 'terminal':
            return input[self.symbol]
        else:
            if(self.right is not None):
                return self.conversor.convert(self.symbol, self.left.run(input), self.right.run(input))
            else:
                return self.conversor.convert(self.symbol, self.left.run(input), None)

    def show(self, index=0):
        print(index, self.symbol)
        if self.left is not None:
            self.left.show(index+1)
        if self.right is not None:
            self.right.show(index+1)

def soma(a,b):
    return a+b
def subtracao(a,b):
    return a-b
def multiplicacao(a,b):
    return a*b
def divisao(a,b):
    return a/b
def sqrt(a,b):
    return np.sqrt(a)
def log(a,b):
    return np.log(a)
def sin(a,b):
    return np.sin(a)
def cos(a,b):
    return np.cos(a)
def tan(a,b):
    return np.tan(a)
def pow(a,b):
    return np.power(a, b)

primitivas = {'+':soma, '-':subtracao, '*':multiplicacao,
            '/':divisao, 'sqrt':sqrt, '^':pow, 'log':log,
            'sin':sin, 'cos':cos, 'tan':tan
            }

class Conversor(object):
    def __init__(self):
        self.primitivas = primitivas
    def convert(self, symbol, a, b):
        return self.primitivas[symbol](a,b)
