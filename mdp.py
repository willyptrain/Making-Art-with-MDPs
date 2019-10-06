import numpy as np
import math
import sys

class MDP:
	def __init__(self, grid): #add parameter for exit_coordinates
		self.height = len(grid)
		self.width = len(grid[0])
		self.grid = np.array(grid)
		self.values = np.zeros(shape=(self.height+2,self.width+2))
		self.nodes = np.array(grid)
		self.action_abilities = {0: "up", 1: "left", 2: "right", 3:"down"}
		self.action_rewards = []
		'''self.nodes.append(np.array([[0, 0.8, 0], [0.1, 0, 0.1], [0, 0, 0]])) #use 0.8, 0.1, 0.1...or just the 1?
		self.nodes.append(np.rot90(self.nodes[0]))
		self.nodes.append(np.fliplr(self.nodes[1]))
		'''
		#list(zip(np.where(self.nodes == -1)[0],np.where(self.nodes == -1)[1]))
		# self.exit_coordinates = {"-1":[], "1": []} 
		self.best_policy = []
		self.max_rewards = np.zeros(shape=(self.height,self.width))
		finished = False

	def update_values(self):
		living_reward = -0.01
		old_values = self.values
		new_values = np.zeros(shape=(self.height+2, self.width+2))
		#new_values.fill(math.pi)
		# temp = self.nodes[1:len(new_values)-1, 1:len(new_values[0])-1]
		new_values[1: len(new_values)-1, 1:len(new_values[0])-1] = self.nodes
		np.place(new_values, new_values == 0, math.pi)
		#new_values[1: len(new_values)-1, 1:len(new_values[0])-1] = living_reward + self.max_rewards
		np.place(new_values, (abs(new_values) < 1), living_reward+self.max_rewards)
		# for i in self.exit_coordinates["-1"]:
		# 	new_values[i[0]][i[1]] = -1
		# for i in self.exit_coordinates["1"]:
		# 	new_values[i[0]][i[1]] = 1
		self.values = new_values
		
		print(self.max_rewards)
		
	def convolve(self):
		modified_values = np.zeros(shape=(self.height, self.width))
		self.max_rewards = np.zeros(shape=(self.height, self.width))
		self.best_policy = []
		# for r in range(1, len(self.values)-1):
		# 	for c in range(1, len(self.values[r])-1):
		# 		switch_indexes = []
		# 		bound_box = self.values[r-1:r+2, c-1:c+2]
		# 		for r2 in range(0, len(bound_box)):
		# 			for c2 in range(0, len(bound_box[r2])):
		# 				if(bound_box[r2][c2] == math.pi):
		# 					switch_indexes.append([r2, c2])

		for r in range(1, len(self.values)-1):
			for c in range(1, len(self.values[r])-1):
				self.action_rewards = []
				bound_box = self.values[r-1:r+2, c-1:c+2]
				np.place(bound_box, bound_box == math.pi, 0)
				# print(bound_box)
				#Below is for calculating element-wise product for each direction's reward in the grid
				self.action_rewards.append(np.array([[0.1, 0.95, 0.1], [0.1, 0.1, 0.1], [0.1, 0.1, 0.1]])) 
				self.action_rewards.append(np.rot90(self.action_rewards[0]))
				self.action_rewards.append(np.fliplr(self.action_rewards[1]))
				self.action_rewards.append(np.rot90(self.action_rewards[1]))
				element_rewards = [np.sum(np.multiply(action, bound_box)) for action in self.action_rewards]
				self.best_policy.append(self.action_abilities[np.argmax(element_rewards)])
				self.max_rewards[r-1][c-1] = np.amax(element_rewards)
				# print([max(action)element_rewards)
				# computing Hadamard product (element-wise matrix multiplication):
		

		# 		elem_sums = []
		# 		r_center = int((len(self.nodes)-1)/2)
		# 		c_center = int((len(self.nodes[r_center])-1)/2)
		# 		index = 0
		# 		for a in range(0, len(self.nodes)):
		# 			self.nodes[r_center][c_center] = 0
		# 			for i in switch_indexes:
		# 				self.nodes = np.array(self.nodes)
		# 				prob_dir = self.nodes[i[0],i[1]].copy()
		# 				self.nodes[i[0],i[1]] = 0
		# 				self.nodes[r_center][c_center] += prob_dir
		# 			elem_sums.append(np.sum(np.multiply(self.nodes[a],bound_box)))
		# 		self.max_rewards[r-1][c-1] = np.amax(elem_sums)#np.sum(np.multiply(nodes[a],bound_box))
		# 		largest_index = np.argmax(elem_sums)
		# 		modified_values[r-1][c-1] = np.amax(elem_sums)
		# 		self.best_nodes.append(self.action_abilities[largest_index])
		# self.values = modified_values

	def train(self):
		self.update_values()
		orig_values = self.values.copy()
		for i in range(0, 100):
			#print(mdp.values)
			self.update_values()
			#print(mdp.values)
			self.convolve()
		self.update_values()
		self.best_policy = np.array(self.best_policy).reshape(self.height,self.width)
		print(self.values)
		#print(mdp.values[1:len(orig_values)-1,1:len(orig_values)-1])


def welcome_page():
	print("")
	print("")
	print("--Welcome--")
	print("")
	("Enter choice from options below")
	print("1 - Quit")
	print("2 - New Markov decision process")
	choice = input("Choice: ")
	print("")
	handle_selection(choice)

def create_list():
	print("Creating New List")
	print("")
	height = 0
	width = 0
	x = []
	y = []
	dimension = input("Enter the dimensions for your grid (i.e. 2,2 or 10,10):  ") 
	if(dimension.split(",")[0].isdigit()):
		if(dimension.split(",")[1].isdigit()):
			height = int(dimension.split(",")[0])
			width = int(dimension.split(",")[1])
			if(height > 1 and width > 1):
				print("Creating grid of dimensions " + str(height) + " x " + str(width))
				print("Enter values:")
				for i in range(0, height):
					x_row = input("Enter values, separated by a comma: ")
					x_row = np.array(x_row.split(","))
					if(len(x_row) > width or len(x_row) < width):
						print("Wrong dimensions or improperly formatted. Make sure your number of values equals your specified dimensions")
					else:
						x.append(x_row.astype(int))
				x = np.array(x)
				mdp = MDP(x)
				#print(mdp)
				mdp.train()
				print(mdp.best_nodes)
			else:
				print("Use dimensions greater than 1 x 1")
		else:
			print("Could not create list from given dimensions. Try again.")
	else:
		print("Could not create list from given dimensions. Try again.")

def handle_selection(choice):
	if(not choice.isdigit()):
		print("Please enter a digit")
	else:
		x = int(choice)
		if(x == 1):
			sys.exit()
		elif(x == 2):
			create_list()
		else:
			second_choice = input("Not an option. Enter new choice: ")
			handle_selection(second_choice)


if __name__ == '__main__':
	mdp = MDP([[-1,-1,-1, -1], [0,0,0,1], [-1,-1,-1, -1]])
	# mdp = MDP([[-1, 0], [1, 0]])
	print(mdp.grid)
	mdp.train()
	print(mdp.best_policy)
	#welcome_page()
	# print(mdp.best_nodes)


'''
		 0.54437251  0.101       0.54437251
		 1.          0.92351505 -1.        
		 1.0012499   0.91761946  0.72990655

		'up',	 	'right'  	'up'
		'left'		'left' 		'left'
		'up'		'up'		'left'

		-> Returns right at index (0, 1) because value at index (0, 2) == (0,0 ) and right comes after left

'''



