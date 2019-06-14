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
		self.population = [initialize(self.terminal_symb, self.primitive_symbol) for i in range(self.size)]

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

	def select_node(self, t):
		prob = random.random()
		if prob>=0.9:
			return t
		if (t.left is None) and (t.right is None):
			return None
		if t.left is not None:
			return self.select_node(t.left)
		if t.right is not None:
			return self.select_node(t.right)


	def crossover(self, idx1, idx2):
		t1, t2 = self.population[idx1], self.population[idx2]
		gene1 = self.select_node(t1)
		while(gene1 is None):
			gene1 = self.select_node(t1)
		gene2 = self.select_node(t2)
		while(gene2 is None):
			gene2 = self.select_node(t2)

		p1, p2 = gene1.up, gene2.up #Pai do nó escolhido
		if p1 is None: #Cromossomo 1 completamente selecionado
			self.population[idx1] = gene2
		elif p1.left==gene1 :#gene1 é filho esquerdo
			p1.left = gene2
		else:			#gene1 é filho direito
			p1.right = gene2
		gene2.up = p1

		if p2 is None: #Cromossomo 2 completamente selecionado
			self.population[idx2] = gene1
		elif p2.left==gene2:
			p2.left = gene1
		else:
			p2.right = gene1
		gene1.up = p2

	def mutation(self, idx):
		t = self.population[idx]
		gene = self.select_node(t)
		while gene is None:
			gene = self.select_node(t)
		parent = gene.up

		mutated_gene = initialize(self.terminal_symb, self.primitive_symbol)
		if parent is None:
			self.population[idx] = mutated_gene
		elif parent.left == gene:
			parent.left = mutated_gene
		else:
			parent.right = mutated_gene
		mutated_gene.up = parent