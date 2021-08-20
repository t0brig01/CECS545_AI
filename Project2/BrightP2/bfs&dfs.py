import sys
import math
from itertools import permutations 
import matplotlib.pyplot as pypl
import time

cities = []
bfs = []
dfs = []


class city:
    def __init__(self, number, x, y,nextCities):
        self.number = number
        self.x = x
        self.y = y
        self.nextCities = nextCities 
        
def breadthFirst(listOfCities):
    minNext = 1
    for city in listOfCities:
        if(minNext == city.number):
            bfs.append(city)
            minDist = 999
            for x in city.nextCities:
                dist = calcDistance(listOfCities[x-1],city)
                if (dist < minDist):
                    minDist = dist
                    minNext = x

def parseFile(fileName):
    with open(fileName) as file:
        if (file == None):
            print("File not found")
        for x in range(7): #skip passed all that header 
            file.next()
        num = 0
        for line in file:
            num += 1
            splitLine = line.split(' ')
            if(splitLine[0] == '1'):
                cities.append(city(int(splitLine[0]),float(splitLine[1]),float(splitLine[2]),[2,3,4]))
            if(splitLine[0] == '2'):
                cities.append(city(int(splitLine[0]),float(splitLine[1]),float(splitLine[2]),[3]))
            if(splitLine[0] == '3'):
                cities.append(city(int(splitLine[0]),float(splitLine[1]),float(splitLine[2]),[4,5]))
            if(splitLine[0] == '4'):
                cities.append(city(int(splitLine[0]),float(splitLine[1]),float(splitLine[2]),[5,6,7]))
            if(splitLine[0] == '5'):
                cities.append(city(int(splitLine[0]),float(splitLine[1]),float(splitLine[2]),[7,8]))
            if(splitLine[0] == '6'):
                cities.append(city(int(splitLine[0]),float(splitLine[1]),float(splitLine[2]),[8]))
            if(splitLine[0] == '7'):
                cities.append(city(int(splitLine[0]),float(splitLine[1]),float(splitLine[2]),[9,10]))
            if(splitLine[0] == '8'):
                cities.append(city(int(splitLine[0]),float(splitLine[1]),float(splitLine[2]),[9,10,11]))
            if(splitLine[0] == '9'):
                cities.append(city(int(splitLine[0]),float(splitLine[1]),float(splitLine[2]),[11]))
            if(splitLine[0] == '10'):
                cities.append(city(int(splitLine[0]),float(splitLine[1]),float(splitLine[2]),[11]))
            if(splitLine[0] == '11'):
                cities.append(city(int(splitLine[0]),float(splitLine[1]),float(splitLine[2]),[]))


def calcDistance(c1,c2): #Distance calculations this time in a *function*
    dist = math.sqrt(math.pow(float(c2.x)-float(c1.x),2) + math.pow(float(c2.y)-float(c1.y),2)) 
    return dist

def formatAndShow(cities):
    formatx = []
    formaty = []
    for num in cities:
        formatx.append(num.x)
        formaty.append(num.y)    
    pypl.plot(formatx,formaty,marker ='o')
    pypl.show()

def depthFirst(cities):
    minNext = 1
    for city in cities:
        if(minNext == city.number):
            dfs.append(city)
            if(city.nextCities):
                minNext = city.nextCities[0]
def main(argv):
    timer = time.time()
    if (len(argv) < 2):
        print("No file name inputted") #Error handling
        sys.exit(1)
    parseFile(argv[1]) #Parse file based on file name provided
    print("Depth First Search")
    depthFirst(cities)
    print("----------Path-----------")
    minPathNums = []
    for x in dfs:
        minPathNums.append(x.number)
    print(minPathNums)
    print("Breadth First Search")
    breadthFirst(cities)
    print("----------Path-----------")
    minPathNums = []
    for x in bfs:
        minPathNums.append(x.number)
    print(minPathNums)
    print("-------Time Elasped-------")
    print("{0} seconds".format(time.time() - timer))
    formatAndShow(bfs)
    formatAndShow(dfs)


if (__name__ == '__main__'):
    main(sys.argv)