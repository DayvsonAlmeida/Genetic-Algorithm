from utils import initialize
from genetic import GA
import numpy as np
import argparse
import random
import time
import sys

sys.setrecursionlimit(2000)
random.seed(time.time())
parser = argparse.ArgumentParser()
parser.add_argument('--mr', help='Mutation Rate')
parser.add_argument('--cr', help='Crossover Rate')
parser.add_argument('--size', help='Population Size')
parser.add_argument('--ngen', help='Number of Generations')
parser.add_argument('--base', help='Base de Teste [Easy, Medium, Hard, Newton, Einstein, Pythagorean]')
args, unknown = parser.parse_known_args()
#cls && python main.py --mr 0.05 --cr 0.8 --size 100 --ngen 5000 --base Easy
mutation_rate = float(args.mr)
crossover_rate = float(args.cr)
size = int(args.size)
ngen = int(args.ngen)
test = args.base


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
				'y':np.array(np.random.randint(100), dtype='float64'),#, dtype='float64'),
				'z':np.array(np.random.randint(100), dtype='float64')}#, dtype='float64')}
hard['y'] = np.sin(hard['x']['x']) + hard['x']['y']**0.5 - np.tan(hard['x']['z'] + hard['x']['x'])
hard['terminal_symb'] = ['x','y','z']

#Pythagorean Theorem
# c² = a²+b²
pythagorean_theorem = {}
pythagorean_theorem['x'] = {'a': np.array(np.random.randint(100, size=100), dtype='float64'),
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
					'm2': np.array(np.random.randint(100, size=100), dtype='float64'),
					'd': np.array(np.random.randint(100, size=100)+np.random.rand(100)+10E-11, dtype='float64')}
newton_law['y'] = (newton_law['x']['m1']*newton_law['x']['m2']*G)/(newton_law['x']['d']**2)
newton_law['terminal_symb'] = ['m1','m2','d']

base = {'Easy': easy, 'Pythagorean':pythagorean_theorem,
		'Medium': medium, 'Hard': hard,
		'Newton': newton_law,
		"Einstein": einstein_relativity}


ga = GA(terminal_symb=base[test]['terminal_symb'], x=base[test]['x'], y=base[test]['y'], size=size,
		num_generations=ngen, crossover_rate=crossover_rate, mutation_rate=mutation_rate, early_stop=0.1)
ga.run()
#print('\n\n\nBest Cromossome')
#ga.bestCromossome.show()
