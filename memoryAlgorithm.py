import csv
import random

class memoryFilter():
    def _init_(self):
        pass
    
    def addMemory(self, memoryData):
        self.memoryData = memoryData
        self.databasePath = "imageDatabase/database.csv"

        with open(self.databasePath, mode='a', newline="") as memoryFile:
            self.memoryFile = csv.writer(memoryFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            self.memoryFile.writerow(self.memoryData + [3])

    def changeMemoryPosition(self, memoryName, answerRatio):
        self.memoryName = memoryName
        self.answerRatio = answerRatio
        self.databasePath = "imageDatabase/database.csv"
        self.memories = []
        self.count = 0

        with open(self.databasePath) as memoryFile:
            self.memoryFile = csv.reader(memoryFile)

            for line in self.memoryFile:
                if line[1] == self.memoryName:
                    self.memoryPos = self.count
                    print(self.memoryPos)

                self.memories.append(line)
                self.count += 1

        if self.answerRatio[0]/(sum(self.answerRatio)) <= 1/5:
            self.memories[self.memoryPos][-1] = 1
        elif 1/5 < self.answerRatio[0]/(sum(self.answerRatio)) <= 2/5:
            self.memories[self.memoryPos][-1] = 2
        elif 2/5 < self.answerRatio[0]/(sum(self.answerRatio)) <= 3/5:
            self.memories[self.memoryPos][-1] = 3
        elif 3/5 < self.answerRatio[0]/(sum(self.answerRatio)) <= 4/5:
            self.memories[self.memoryPos][-1] = 4
        elif 4/5 < self.answerRatio[0]/(sum(self.answerRatio)):
            self.memories[self.memoryPos][-1] = 5

        self.f = open(self.databasePath, "w")
        self.f.truncate()
        self.f.close()

        

        with open(self.databasePath, mode='a', newline="") as memoryFile:
            self.memoryFile = csv.writer(memoryFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            for i in self.memories:
                self.memoryFile.writerow(i)

            memoryFile.close()

        

    def pickMemory(self):
        self.memoryList = []
        self.databasePath = "imageDatabase/database.csv"

        with open(self.databasePath) as memoryFile:
            self.memoryFile = csv.reader(memoryFile)

            for line in self.memoryFile:
                if line[-1] == "1":
                    for i in range(5):
                        self.memoryList.append(line)
                elif line[-1] == "2":
                    for i in range(4):
                        self.memoryList.append(line)
                elif line[-1] == "3":
                    for i in range(3):
                        self.memoryList.append(line)
                elif line[-1] == "4":
                    for i in range(2):
                        self.memoryList.append(line)
                elif line[-1] == "5":
                    for i in range(1):
                        self.memoryList.append(line)

        return(random.choice(self.memoryList))

        

algo = memoryFilter()

print(algo.pickMemory())



