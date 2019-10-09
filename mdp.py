import numpy as np
import math
import sys

class MDP:
	def __init__(self, grid): 
		self.height = len(grid)
		self.width = len(grid[0])
		self.grid = np.array(grid)
		self.values = np.zeros(shape=(self.height+2,self.width+2))
		self.nodes = np.array(grid)
		self.action_abilities = {0: "up", 1: "left", 2: "right", 3:"down"}
		self.action_rewards = []
		self.best_policy = []
		self.max_rewards = np.zeros(shape=(self.height,self.width))
		finished = False

	def update_values(self):
		living_reward = -0.01
		old_values = self.values
		new_values = np.zeros(shape=(self.height+2, self.width+2))
		np.place(new_values, new_values == 0, math.pi)
		new_values[1: len(new_values)-1, 1:len(new_values[0])-1] = self.nodes
		np.place(new_values, (abs(new_values) < 1), living_reward+self.max_rewards)
		self.values = new_values
		
		
	def convolve(self):
		modified_values = np.zeros(shape=(self.height, self.width))
		self.max_rewards = np.zeros(shape=(self.height, self.width))
		self.best_policy = []
		for r in range(1, len(self.values)-1):
			for c in range(1, len(self.values[r])-1):
				self.action_rewards = []
				bound_box = self.values[r-1:r+2, c-1:c+2]
				np.place(bound_box, bound_box == math.pi, 0)
				self.action_rewards.append(np.array([[0.0, 0.95, 0.0], [0.0, 0.02, 0.0], [0.0, 0.0, 0.0]])) 
				self.action_rewards.append(np.rot90(self.action_rewards[0]))
				self.action_rewards.append(np.fliplr(self.action_rewards[1]))
				self.action_rewards.append(np.rot90(self.action_rewards[1]))
				element_rewards = [np.sum(np.multiply(action, bound_box)) for action in self.action_rewards]
				self.best_policy.append(self.action_abilities[np.argmax(element_rewards)])
				self.max_rewards[r-1][c-1] = np.amax(element_rewards)
				self.nodes[r-1][c-1] = np.amax(element_rewards)
		

	def train(self):
		self.update_values()
		orig_values = self.values.copy()
		for i in range(0, 10):
			self.update_values()
			self.convolve()
		self.update_values()
		self.best_policy = np.array(self.best_policy).reshape(self.height,self.width)

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
				mdp.train()
				print(mdp.best_policy)
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
	welcome_page()




