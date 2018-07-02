import numpy as np

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
		self.living_reward = -0.1
		self.discount = 0.9
		self.exit_coordinates = {"-1": [[1+1,2+1]], "1": [[0+1,2+1]]}
		self.best_actions = []
		self.max_rewards = np.zeros(shape=(height,width))

	def update_values(self, t):
		old_values = self.values
		new_values = np.zeros(shape=(self.height+2, self.width+2))
		new_values[1: len(new_values)-1, 1:len(new_values[0])-1] = old_values[1:len(self.values)-1, 1:len(self.values)-1] + (self.discount**t)*self.max_rewards
		for i in self.exit_coordinates["-1"]:
			new_values[i[0]][i[1]] = "-1"
		for i in self.exit_coordinates["1"]:
			new_values[i[0]][i[1]] = "1"

		self.values = new_values
		
	def convolve(self):
		modified_values = np.zeros(shape=(self.height, self.width))
		self.max_rewards = np.zeros(shape=(self.height, self.width))
		self.best_actions = []
		for r in range(1, len(self.values)-1):
			for c in range(1, len(self.values[r])-1):
				bound_box = self.values[r-1:r+2, c-1:c+2]
				largest = np.sum(np.multiply(self.actions[0], bound_box))
				largest_index = 0
				for y in range(1, len(self.actions)):
					temp_value = 0
					temp_value = np.sum(np.multiply(self.actions[y], bound_box))
					#print(self.action_abilities[y])
					#print(temp_value)
					if(temp_value > largest):
						largest = temp_value
						largest_index = y
				self.max_rewards[r-1][c-1] = temp_value
				modified_values[r-1][c-1] = largest
				self.best_actions.append(self.action_abilities[largest_index])
				
		self.values = modified_values





if __name__ == '__main__':
	mdp = MDP(3,3)
	for i in range(0, 10):
		#print(mdp.values)
		mdp.update_values(i)
		#print(mdp.values)
		mdp.convolve()
		break
	mdp.update_values(11)
	print(mdp.values[1:len(mdp.values)-1,1:len(mdp.values[0])-1])
	#print(mdp.best_actions)
	for i in range(0, mdp.height):
		print(mdp.best_actions[i:i+3])
	'''
		Example;
			
			0	0	0	0	0
			
			0	0	0	1	0
			
			0	0	0	-1	0
	
			0	0	0	0	0





	'''



