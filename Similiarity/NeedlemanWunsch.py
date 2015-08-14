__author__ = 'Konrad Kopciuch'

from Bio.SubsMat import MatrixInfo as mi


class NeedlemanWunsch:

    def __init__(self, seq1, seq2):
        self.seq1 = seq1
        self.seq2 = seq2
        self.__initialize_points_matrix()
        self.initialize_directions_matrix()
        self.calculate_matrix()

    def __initialize_points_matrix(self):
        self.pointsMatrix = createZeroesMatrix(len(self.seq1)+1, len(self.seq2)+1)
        self.pointsMatrix[0][0] = 0
        for i in range(len(self.seq1)+1):
            self.pointsMatrix[i][0] = i * self.getPointForBreak()
        for i in range(len(self.seq2)+1):
            self.pointsMatrix[0][i] = i * self.getPointForBreak()

    def initialize_directions_matrix(self):
        self.directionsMatrix = createZeroesMatrix(len(self.seq1)+1, len(self.seq2)+1)

    def calculate_matrix(self):
        for x in range(len(self.seq1)):
            for y in range(len(self.seq2)):
                i,j = x+1,y+1
                match = self.calculatePointsForMatch(i,j)
                delete = self.calculatePointsForDelete(i,j)
                insert = self.calculatePointsForInsert(i,j)
                value = max((match, delete, insert))

                self.directionsMatrix[i][j] = (match == value, delete == value, insert == value)
                self.pointsMatrix[i][j] = value

    def get_solutions(self):
        start_position = (len(self.seq1), len(self.seq2))
        return self.getAllSolutions(start_position, [''], False)

    def getAllSolutions(self, position, partialSolutions, canStop):
        if position[0] ==0 or position[1] == 0:
            if canStop:
                return partialSolutions
            else:
                return [] #bledna sciezka

        canStop = position == (1,1)
        allSolutions = []

        directionList = self.directionsMatrix[position[0]][position[1]]
        if directionList[0]: #match
            newPosition = (position[0]-1,position[1]-1)
            newElement = '('+ self.seq1[position[0]-1] +',' + self.seq2[position[1]-1] +')'
            newSolutions = self.joinSolutions(newElement, partialSolutions)
            allSolutions.extend(self.getAllSolutions(newPosition, newSolutions, canStop))
        if directionList[1]: #delete
            newPosition = (position[0]-1,position[1])
            newElement = '(-,'+ self.seq2[position[1]-1] +')'
            newSolutions = self.joinSolutions(newElement, partialSolutions)
            allSolutions.extend(self.getAllSolutions(newPosition, newSolutions, canStop))
        if directionList[2]: #insert
            newPosition = (position[0],position[1]-1)
            newElement = '('+ self.seq1[position[0]-1] +',-)'
            newSolutions = self.joinSolutions(newElement, partialSolutions)
            allSolutions.extend(self.getAllSolutions(newPosition, newSolutions, canStop))

        return allSolutions

    def joinSolutions(self, newElement, oldSolutions):
        newSolutions = []
        for solution in oldSolutions:
            newSolutions.append(newElement + solution)
        return newSolutions

    def calculatePointsForMatch(self, i, j):
        A = self.seq1[i-1]
        B = self.seq2[j-1]
        return self.pointsMatrix[i-1][j-1] + self.getPointForMatch(A,B)

    def calculatePointsForDelete(self, i, j):
        return self.pointsMatrix[i-1][j] + self.getPointForBreak()

    def calculatePointsForInsert(self, i, j):
        return self.pointsMatrix[i][j-1] + self.getPointForBreak()

    def getPointForMatch(self, a, b):
        if a==b:
            return 4
        return -4

    def getPointForBreak(self):
        return -7

#n - number of rows, m - number of colums
def createZeroesMatrix(n,m):
	return [[None]*m for i in range(n)]

seq1 = "GAUGCG"
seq2 = "CAUCG"
alg = NeedlemanWunsch(seq1, seq2)
s = alg.get_solutions()
print s
