from utils import initialize
from genetic import GA
import numpy as np
import random
import time
import sys

sys.setrecursionlimit(2000)

random.seed(time.time())

# f(x) = 2*x
easy = {}
easy['x'] = {'a':np.array(np.arange(100), dtype='float64')}
easy['y'] = easy['x']['a']*2
easy['terminal_symb'] = ['a']

# f(x,y,z) = sqrt(x+y)+z
medium = {}
medium['x'] = {'x':np.array(np.arange(100), dtype='float64'),
				'y':np.array(np.random.randint(100)),#, dtype='float64'),
				'z':np.array(np.random.randint(100))}#, dtype='float64')}
medium['y'] = (medium['x']['x']+medium['x']['y'])**0.5 + medium['x']['z']
medium['terminal_symb'] = ['x','y','z']

# f(x,y,z) = sin(x)+sqrt(y)-tan(z+x)
hard = {}
hard['x'] = {'x':np.array(np.arange(100), dtype='float64'),
				'y':np.array(np.random.randint(100)),#, dtype='float64'),
				'z':np.array(np.random.randint(100))}#, dtype='float64')}
hard['y'] = np.sin(hard['x']['x']) + hard['x']['y']**0.5 - np.tan(hard['x']['z'] + hard['x']['x'])
hard['terminal_symb'] = ['x','y','z']

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
		'Medium': medium, 'Hard': hard,
		'Newton Law of Gravitation': newton_law,
		"Einstein's Relativity": einstein_relativity}


size = 20
test = 'Hard'
ga = GA(terminal_symb=base[test]['terminal_symb'], x=base[test]['x'], y=base[test]['y'], size=size,
		num_generations=2000, crossover_rate=0.7, mutation_rate=0.05, early_stop=0.1)
ga.run()
#print('\n\n\nBest Cromossome')
#ga.bestCromossome.show()
