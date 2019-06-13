from utils import initialize
import numpy as np
import random
import sys

class GA(object):
	def __init__(self, terminal_symb, x, y, size, num_generations=1000, crossover_rate=0.7, mutation_rate=0.05, early_stop=0.1):
		self.primitive_symbol = ['+','-','*','/','sqrt','^','log','sin','cos','tan']
		self.terminal_symb = terminal_symb
		self.x = x
		self.y = y

		self.size = size
		self.num_generations = num_generations
		self.early_stop = early_stop
		self.crossover_rate = crossover_rate
		self.mutation_rate = mutation_rate
		self.population = [initialize(terminal_symb, self.primitive_symbol) for i in range(self.size)]

	def fitness(self):
		outputs = [self.population[i].run(self.x) for i in range(self.size)]
		error = [((outputs[i]-self.y)**2).mean() for i in range(self.size)]
		error = np.array(error)
		#Replace nan, inf and overflow with max int value
		where_are_NaNs = np.isnan(error)
		error[where_are_NaNs] = sys.maxsize/self.size
		where_are_infs = (error == np.inf)
		error[where_are_infs] = sys.maxsize/self.size
		where_are_negative = (error < 0)
		error[where_are_negative] = sys.maxsize/self.size

		return error

	def select(self, t):
		prob = random.random()
		if prob>=0.75:
			return t
		if (t.left is None) and (t.right is None):
			return None
		if t.left is not None:
			return self.select(t.left)
		if t.right is not None:
			return self.select(t.right)


	def crossover(self, t1, t2):
		s1 = self.select(t1)
		while(s1 is None):
			s1 = self.select(t1)
		s2 = self.select(t2)
		while(s2 is None):
			s2 = self.select(t2)
		#Not implemented
		return s1,s2
