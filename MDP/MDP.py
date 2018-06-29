import numpy as np

class MDP:
	def __init__(self, height, width): #add parameter for exit_coordinates
		self.values = np.zeros(shape=(height+2,width+2))
		self.actions = []
		self.height = height
		self.width = width
		self.action_abilities = ["up", "right", "left"]
		self.actions.append(np.array([[0, 0.8, 0], [0.1, 0, 0.1], [0, 0, 0]]))
		self.actions.append(np.rot90(self.actions[0]))
		self.actions.append(np.fliplr(self.actions[1]))
		self.living_reward = -0.01
		self.discount = 0.9
		self.exit_coordinates = {"-1": [[0+1,2+1]], "1": [[1+1,2+1]]}

	def update_values(self):
		old_values = self.values
		new_values = np.zeros(shape=(self.height+2, self.width+2))
		new_values[1: len(new_values)-1, 1:len(new_values[0])-1] = self.living_reward + self.discount*old_values[1:len(self.values)-1, 1:len(self.values)-1]

		for i in self.exit_coordinates["-1"]:
			new_values[i[0]][i[1]] = "-1"
		for i in self.exit_coordinates["1"]:
			new_values[i[0]][i[1]] = "1"	
			
		self.values = new_values
		
	def convolve(self):
		pass


if __name__ == '__main__':
	mdp = MDP(3,3)
	print(mdp.values)
	mdp.update_values()
	print(mdp.values)


