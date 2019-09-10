import numpy as np
import math

class MDP:
	def __init__(self, height, width): #add parameter for exit_coordinates
		self.values = np.zeros(shape=(height+2,width+2))
		self.actions = []
		self.height = height
		self.width = width
		self.action_abilities = {0: "up", 1: "left", 2: "right"}
		self.actions.append(np.array([[0, 0.8, 0], [0.1, 0, 0.1], [0, 0, 0]])) #use 0.8, 0.1, 0.1...or just the 1?
		self.actions.append(np.rot90(self.actions[0]))
		self.actions.append(np.fliplr(self.actions[1]))
		self.living_reward = -0.01
		self.discount = 1
		self.exit_coordinates = {"-1": [[1+1,2+1]], "1": [[1+1,0+1]]}
		self.best_actions = []
		self.max_rewards = np.zeros(shape=(height,width))
		self.finished = False

	def update_values(self):
		old_values = self.values
		new_values = np.zeros(shape=(self.height+2, self.width+2))
		new_values.fill(math.pi)
		new_values[1: len(new_values)-1, 1:len(new_values[0])-1] = self.living_reward + self.max_rewards

		for i in self.exit_coordinates["-1"]:
			new_values[i[0]][i[1]] = -1
		for i in self.exit_coordinates["1"]:
			new_values[i[0]][i[1]] = 1
		#print(new_values)
		self.values = new_values
		
	def convolve(self):
		modified_values = np.zeros(shape=(self.height, self.width))
		self.max_rewards = np.zeros(shape=(self.height, self.width))
		self.best_actions = []
		for r in range(1, len(self.values)-1):
			for c in range(1, len(self.values[r])-1):
				bound_box = self.values[r-1:r+2, c-1:c+2]
				switch_indexes = []
				for r2 in range(0, len(bound_box)):
					for c2 in range(0, len(bound_box[r2])):
						if(bound_box[r2][c2] == math.pi):
							switch_indexes.append([r2, c2])
				self.actions = []
				self.actions.append(np.array([[0, 0.8, 0], [0, 0, 0], [0.1, 0, 0.1]])) #use 0.8, 0.1, 0.1...or just the 1?
				self.actions.append(np.rot90(self.actions[0]))
				self.actions.append(np.fliplr(self.actions[1]))
				actions = self.actions
				elem_sums = []
				r_center = (len(actions)-1)/2
				c_center = (len(actions[r_center])-1)/2
				index = 0
				for a in range(0, len(self.actions)):
					actions[a][r_center][c_center] = 0
					for i in switch_indexes:
						prob_dir = actions[a][i[0],i[1]].copy()
						actions[a][i[0],i[1]] = 0
						actions[a][r_center][c_center] += prob_dir
					elem_sums.append(np.sum(np.multiply(actions[a],bound_box)))
				self.max_rewards[r-1][c-1] = np.amax(elem_sums)#np.sum(np.multiply(actions[a],bound_box))
				largest_index = np.argmax(elem_sums)
				modified_values[r-1][c-1] = np.amax(elem_sums)
				self.best_actions.append(self.action_abilities[largest_index])
		self.values = modified_values

	def train(self):
		mdp.update_values()
		orig_values = self.values.copy()
		for i in range(0, 10):
			self.update_values()
			self.convolve()
		self.update_values()
		print(mdp.values[1:len(orig_values)-1,1:len(orig_values)-1])
		print(mdp.best_actions[0:3])
		print(mdp.best_actions[3:6])
		print(mdp.best_actions[6:9])


if __name__ == '__main__':
	mdp = MDP(3,3)
	mdp.train()

'''
		 0.54437251  0.101       0.54437251
		 1.          0.92351505 -1.        
		 1.0012499   0.91761946  0.72990655

		'up',	 	'right'  	'up'
		'left'		'left' 		'left'
		'up'		'up'		'left'

		-> Returns right at index (0, 1) because value at index (0, 2) == (0,0 ) and right comes after left

'''



