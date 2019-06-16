from utils import initialize
import numpy as np
import random
import copy
import time
import sys
import os

class GA(object):
	def __init__(self, terminal_symb, x, y, size, num_generations=400, crossover_rate=0.7, mutation_rate=0.05, early_stop=0.1, history_len=20):
		self.primitive_symbol = ['+','-','*','/','sqrt','^','log','sin','cos','tan']
		self.terminal_symb = terminal_symb
		self.x = x
		self.y = y

		self.size = size
		self.history_len = history_len
		self.num_generations = num_generations
		self.early_stop = early_stop
		self.crossover_rate = crossover_rate
		self.mutation_rate = mutation_rate
		self.population = [initialize(self.terminal_symb, self.primitive_symbol) for i in range(self.size)]
		self.status = np.zeros((self.size,),  dtype=int) #Controladora se um cromossomo foi selecionado para a próxima geração
		self.bestCromossome = None
	def fitness(self):
		outputs = [self.population[i].run(self.x) for i in range(self.size)]
		error = [((outputs[i]-self.y)**2).mean() for i in range(self.size)]
		error = np.array(error)
		#Trocando nan, inf e overflow por max int proporcional
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
		t1 = copy.deepcopy(self.population[idx1])
		t2 = copy.deepcopy(self.population[idx2])

		gene1 = self.select_node(t1)
		while(gene1 is None):
			gene1 = self.select_node(t1)
		gene2 = self.select_node(t2)
		while(gene2 is None):
			gene2 = self.select_node(t2)

		p1, p2 = gene1.up, gene2.up #Pai do nó escolhido
		if p1 is None: #Cromossomo 1 completamente selecionado
			t1 = gene2
			#self.population[idx1] = gene2
		elif p1.left==gene1 :#gene1 é filho esquerdo
			p1.left = gene2
		else:			#gene1 é filho direito
			p1.right = gene2
		gene2.up = p1

		if p2 is None: #Cromossomo 2 completamente selecionado
			t2 = gene1
			#self.population[idx2] = gene1
		elif p2.left==gene2:
			p2.left = gene1
		else:
			p2.right = gene1
		gene1.up = p2

		return [t1, t2]

	def mutation(self, idx):
		t = copy.deepcopy(self.population[idx])
		gene = self.select_node(t)
		while gene is None:
			gene = self.select_node(t)
		parent = gene.up

		mutated_gene = initialize(self.terminal_symb, self.primitive_symbol)
		if parent is None:
			t = mutated_gene
		elif parent.left == gene:
			parent.left = mutated_gene
		else:
			parent.right = mutated_gene
		mutated_gene.up = parent
		return [t]

	def roulette(self, fit, total_fit):
		ticket = np.random.random() #Ticket sorteado
		prob = 1-fit/total_fit #Tickets do indivíduo (quanto menor o fitness melhor)
		if(ticket<=prob):
			return True
		return False

	def new_cromossome(self, error, error_history):
		method_ticket = np.random.random() #Ticket do método sorteado
		std = None
		if len(error_history) == self.history_len:
			std = np.std(error_history)
		if std is not None:
			if std <= 0.1:
				self.mutation_rate += 5E-5*(1-self.mutation_rate-self.crossover_rate)

		if method_ticket <= self.crossover_rate: #Realiza Crossover
			status = False
			idx1, idx2 = False, False
			while status is False:
				idx1 = np.random.randint(0, self.size)
				status = self.roulette(error[idx1], error.sum())

			status = False
			while status is False:
				idx2 = np.random.randint(0, self.size)
				status = self.roulette(error[idx2], error.sum())

			return self.crossover(idx1, idx2)
		elif method_ticket <= self.crossover_rate+self.mutation_rate: #Realiza Mutação
			idx1 = np.random.randint(0, self.size)
			return self.mutation(idx1)
		else: #Realiza seleção de Cromossomos para a próxima geração
			while True:
				idx1 = np.random.randint(0, self.size)
				if self.roulette(error[idx1],error.sum()):# and self.status[idx1] == 0: #Cromossomo selecionado não pode estar na próxima geração
					self.status[idx1] = 1
					return [copy.deepcopy(self.population[idx1])]

	def run(self):
		started_time = time.time()
		print('Genetic History Started!')
		error_history = []
		for i in range(self.num_generations):
			error = self.fitness()
			self.status = np.zeros((self.size), dtype=int)
			new_population = []
			best = np.argmin(error)
			error_min = error.min()
			if len(error_history) < self.history_len:
				error_history.append(error_min)
			else:
				_ = error_history.pop(0)
				error_history.append(error_min)

			self.bestCromossome = self.population[best]
			new_population.append(self.bestCromossome)
			while len(new_population) < self.size:
				for cromossome in self.new_cromossome(error, error_history):
					new_population.append(cromossome)

			if i % int(self.num_generations*0.05)==0:
				print('Generation {} of {} -- Best Fitness: {}'.format(i, self.num_generations, error_min))
			if error.min() <= self.early_stop:
				break
			self.population = new_population
		duration = time.time() - started_time
		print('Duration: {} seconds'.format(duration))
