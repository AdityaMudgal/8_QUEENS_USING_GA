# The python code should have the following components
# a. Code must follow Object Oriented program standards with appropriate Unit tests
# b. Function to generate the initial population
# c. Function to score the population
# d. Function to do cross over and mutation of the selected gene pool
# e. Main function to identify the right sequence


import random
import numpy as np
from numpy.random import choice
import pandas as pd


class GA:


	def __init__(self, nQueens, totalPopulation, crossOver, mutationRate):
		self.nQueens = nQueens
		self.totalPopulation = totalPopulation
		self.crossOver = crossOver
		self.mutationRate = mutationRate
		
		self.alpha_list = [x for x in range(0, nQueens)]
			
	
	def initialPopulation(self):
	
		populationData = []
		fitnessData = []
		secure_random = random.SystemRandom()
		for outloop in range(self.totalPopulation):
			randomData = []
			fitnessScore = 28
			for inloop1 in range(self.nQueens):
				selectedData = secure_random.choice(self.alpha_list)
				randomData.append(selectedData)
			populationData.append(randomData)
			for i in range(len(randomData)):
				for j in range(i+1, len(randomData)):
					if (randomData[i]==randomData[j]):
						fitnessScore = fitnessScore - 1
			for i in range(len(randomData)):
				for j in range(i+1, len(randomData)):
					if (abs(randomData[i]-randomData[j]) == abs(i-j)):
						fitnessScore = fitnessScore - 1
			fitnessData.append(fitnessScore)
		probabilityDist = []
		for outloop in range(self.totalPopulation):
			probabilityDist.append(fitnessData[outloop]/self.nQueens)
		
		probDataFrame = pd.DataFrame({'String':populationData,'FitnessScore':fitnessData,'Probability':probabilityDist})
		probDataFrame = probDataFrame.sort_values(['Probability'],ascending=False)
		probDataFrame = probDataFrame.reset_index(drop=True)
		return secure_random,probDataFrame,populationData
	
		
	
	def maxProb(probabilityDist):
		probabilityList = [f for f in set(probabilityDist)]
		return (probabilityList[len(probabilityList)-2])
	
	
	
	def getFitnessScore(self, data):
		#data = ''.join([elem for elem in data])
		fitnessScore = 28
		for i in range(len(data)):
			for j in range(i+1, len(data)):
				if (data[i]==data[j]):
					fitnessScore = fitnessScore - 1
		for i in range(len(data)):
			for j in range(i+1, len(data)):
				if (abs(data[i]-data[j]) == abs(i-j)):
					fitnessScore = fitnessScore - 1
		return fitnessScore
		
	def viewElement(self,data):
		data = ''.join([str(elem) for elem in data])
		return data
	
	
	def crossoverMutation(self):
		secure_random,probDataFrame,populationData = self.initialPopulation()
		crossOverPoint = int(self.crossOver * self.nQueens)
		generationCount = 1000
		for loop in range(generationCount):
			draw=[]
			draw.append(probDataFrame[0:1]["String"].values[0])
			draw.append(probDataFrame[1:2]["String"].values[0])
			if (self.getFitnessScore(draw[0])==28 | self.getFitnessScore(draw[1])==28):
				#print(self.viewElement(draw[0]),' ',self.viewElement(draw[1]))
				if (self.getFitnessScore(draw[0])==28):
					return draw[0]
					break
				else:
					return draw[1]
				break
			child1 = draw[0][0:crossOverPoint]+draw[1][crossOverPoint:]
			child2 = draw[1][0:crossOverPoint]+draw[0][crossOverPoint:]
			child1[random.randint(0,self.nQueens-1)] = secure_random.choice(self.alpha_list)
			child2[random.randint(0,self.nQueens-1)] = secure_random.choice(self.alpha_list)
			populationData.append(child1)
			populationData.append(child2)
			fitnessData = []
			self.totalPopulation = len(populationData)
			for outloop in range(self.totalPopulation):
				fitnessScore = self.getFitnessScore(populationData[outloop])
				fitnessData.append(fitnessScore)
			probabilityDist = []
			for outloop in range(self.totalPopulation):
				probabilityDist.append(fitnessData[outloop]/sum(fitnessData))
			probDataFrame = pd.DataFrame({'String':populationData,'FitnessScore':fitnessData,'Probability':probabilityDist})
			probDataFrame = probDataFrame.sort_values(['Probability'],ascending=False)
			probDataFrame = probDataFrame.reset_index(drop=True)
			print('Generation ',loop,' ',' Average Fitness Score ',probDataFrame["FitnessScore"].mean(),' ', ''.join([str(elem) for elem in child1]),' ',self.getFitnessScore(child1),''.join([str(elem) for elem in child2]),self.getFitnessScore(child2))
	
	

def main():
		
	totalPopulation = int(input("Enter number of population(Kindly enter an INTEGER): "))

	obj = GA(8, totalPopulation, 0.5, 0.01)
	obj.initialPopulation()
	obj.crossoverMutation()
	sequence = obj.crossoverMutation()
	print("Correct sequence",sequence)
	return sequence
	
main()


