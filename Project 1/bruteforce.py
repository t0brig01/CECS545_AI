import sys
import math
from itertools import permutations 
import matplotlib.pyplot as pypl
import time

cities = []
minDist = 9999999999 #hopefully the min is less than that


class city:
    def __init__(self, number, x, y):
        self.number = number
        self.x = x
        self.y = y

def parseFile(fileName):
    with open(fileName) as file:
        if (file == None):
            print("File not found")
        for x in range(7): #skip passed all that header stuff
            file.next()
        num = 0
        for line in file:
            num += 1
            splitLine = line.split(' ')
            cities.append(city(splitLine[0],splitLine[1],splitLine[2]))

def calcDistance(c1,c2): #Distance calculations this time in a *function*
    dist = math.sqrt(math.pow(float(c2.x)-float(c1.x),2) + math.pow(float(c2.y)-float(c1.y),2)) 
    return dist

def formatAndShow(permut,first):
    formatx = []
    formaty = []
    #throw in first city that was previously popped out of the cities array
    formatx.append(float(first.x))
    formaty.append(float(first.y))
    for num in permut:
        formatx.append(float(num.x))
        formaty.append(float(num.y))
    #connect back to the first city
    formatx.append(float(first.x))
    formaty.append(float(first.y))
    pypl.plot(formatx,formaty,marker ='o')
    pypl.show()

def main(argv):
    timer = time.time()
    if (len(argv) < 2):
        print("No file name inputted") #Error handling
        sys.exit(1)
    parseFile(argv[1]) #Parse file based on file name provided
    firstCity = cities.pop(0) #Remove first city to cut down on number of permutations to decrease runtime
    for x in permutations(cities):
        dist = 0
        count = 0 
        while count <= len(x):
            if(count == 0):
                dist += calcDistance(x[count],firstCity)
            elif(count == len(x)):
                dist += calcDistance(firstCity,x[count-1])
            else:
                dist += calcDistance(x[count-1],x[count])
            count += 1
        global minDist
        if(minDist > dist):
            minDist = dist
            minPerm = x
    print("-------Min Distance-------")
    print(minDist)
    print("-------Min Permutation----")
    minPermNums =[]
    minPermNums.append("1")
    for x in minPerm:
        minPermNums.append(x.number)
    print(minPermNums)
    print("-------Time Elasped-------")
    print("{0} seconds".format(time.time() - timer))
    formatAndShow(minPerm,firstCity)


if (__name__ == '__main__'):
    main(sys.argv)