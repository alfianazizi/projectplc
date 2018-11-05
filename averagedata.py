#module for moving average

class averageData:
	def __init__(self, x, y, z ):
		self.maxPoints = x #Sets the maximum number for the array
		self.varList = [] #Initialize the list
		self.name = z #Name of what is being stored in the list
		self.averagePoints = y #Number of points to average
		
	def updateData(self, newData):
		#if the current length of the list is less then the max length
		#append the new data point to the end of the list
		if(len(self.varList) < self.maxPoints):
			self.varList.append(newData)
		else:
			for x in range (0, len(self.varList)):
				if ((x + 1) < len(self.varList)):
					self.varList[x] = self.varList[x + 1]
				else:
					self.varList[x] = newData
		return
		
	def printList(self):
		#Print the list to the terminal window
		print ('\nPrinting ' + self.name + ' to the terminal.')
		for x in range(0, len(self.varList)):
			print (self.name + '[' + str(x) + ']' + str(self.varList[x]))
		return
	
	def returnList(self):
		#Return the whole list
		return self.varList
	
	def runningAverage(self):
		#Returns the average of the specified number of points
		average = 0.00
		avgList = self.returnList()
		y = len(avgList)
		try:
			if (y < self.averagePoints):
				#If the length of the list is less then the total points
				#to average, just average the number in the list
				for x in range (0, y):
					average = average + float(avgList[x])
				average = average / y
			else:
				#Average the specified number of points
				for x in range (1, (1 + self.averagePoints)):
					average = average + float(avgList[(y-x)])
				average = average / self.averagePoints
		except ZeroDivisionError:
			print ('Division by zero')
			return average
		return average