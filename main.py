from utils import initialize
from genetic import GA
import numpy as np
import random
import time

random.seed(time.time())
#random.seed(7)

#TODO: Verificar tamanho da arvore para não haver problemas com estouro da pilha do python

# f(x) = 2*x
easy = {}
easy['x'] = {'a':np.array(np.arange(100), dtype='float64')}
easy['y'] = easy['x']['a']*2
easy['terminal_symb'] = ['a']

#Pythagorean Theorem
# c² = a²+b²
pythagorean_theorem = {}
pythagorean_theorem['x'] = {'a': np.random.randint(100, size=100),
							'b': np.array(np.arange(100), dtype='float64')}
pythagorean_theorem['y'] = pythagorean_theorem['x']['a']**2 +pythagorean_theorem['x']['b']**2
pythagorean_theorem['terminal_symb'] = ['a','b']

#Einstein's Theory of Relativity
# E = m*c²
# c = 299.792.458 m/s
einstein_relativity = {}
einstein_relativity['x'] = {'m': np.random.random(100)}
einstein_relativity['y'] = einstein_relativity['x']['m']*(299792458**2) #c²=89875517873681764
einstein_relativity['terminal_symb'] = ['m']

#Newton's Universal Law of Gravitation
# F = G*m1*m2/d²
G = 6.674*10E-11
newton_law = {}
newton_law['x'] = {'m1': 10*np.array(np.random.random(100), dtype='float64'),
					'm2': np.random.randint(100, size=100),
					'd': np.random.randint(100, size=100)+np.random.rand(100)+10E-11}
newton_law['y'] = (newton_law['x']['m1']*newton_law['x']['m2']*G)/(newton_law['x']['d']**2)
newton_law['terminal_symb'] = ['m1','m2','d']

base = {'Easy': easy, 'Pythagorean Theorem':pythagorean_theorem,
		'Newton Law of Gravitation': newton_law,
		"Einstein's Relativity": einstein_relativity}


size = 50
ga = GA(terminal_symb=base['Easy']['terminal_symb'], x=base['Easy']['x'], y=base['Easy']['y'], size=size,
		num_generations=400, crossover_rate=0.7, mutation_rate=0.05, early_stop=0.1)
ga.run()
print('\n\n\nBest Cromossome')
ga.bestCromossome.show()