from utils import initialize
from genetic import GA
import numpy as np
import sys

x = {'a':np.array([1,2,3,4,5,6,7,8,9,10,11], dtype='float64'), 'b':np.array([2,2,2,2,2,2,2,2,2,2,2], dtype='float64')}
y = x['a']*x['b']
terminal_symb = ['a','b']


population_size = 2
ga = GA(terminal_symb=terminal_symb, x=x, y=y, size=population_size)
t1, t2=ga.population[0], ga.population[1]
s1, s2 = ga.crossover(t1,t2)

if(s1!=None):
	print('HEY')
if(s2!=None):
	print('Double HEY')

print(s1.type, s2.type)
