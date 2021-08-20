import sys
import math
from itertools import permutations 
import matplotlib.pyplot as pypl
import time

cities = []

class city:
    def __init__(self, number, x, y):
        self.number = number
        self.x = x
        self.y = y
        
class edge:
    def __init__(self,toCity,fromCity):
        self.toCity = toCity
        self.fromCity = fromCity

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
            cities.append(city(int(splitLine[0]),float(splitLine[1]),float(splitLine[2])))


def calcDistance(c1,c2): #Distance calculations this time in a *function*
    dist = math.sqrt(math.pow(c2.x-c1.x,2) + math.pow(c2.y-c1.y,2)) 
    return dist

def formatAndShow(out):
    formatx = []
    formaty = []
    for c in out: 
        formatx.append(c.x)
        formaty.append(c.y)    
        pypl.plot(formatx,formaty,marker ='o')
        pypl.pause(.5)

def main(argv):
    timer = time.time()
    pypl.ion()
    if (len(argv) < 2):
        print("No file name inputted") #Error handling
        sys.exit(1)
    parseFile(argv[1]) #Parse file based on file name provided

    edges = []
    #Because TSP > 4 nodes is trivially solvable, start with 3
    edges.append(edge(cities[0],cities[1])) 
    edges.append(edge(cities[1],cities[2]))
    edges.append(edge(cities[2],cities[0]))
    for city in cities[3:]: #Go through all cities but first 3
        minDist = 999999
        i = 0
        count = 0
        for e in edges: #go through each edges and compares distance
            dist = calcDistance(city,e.fromCity) + calcDistance(city,e.toCity) - calcDistance(e.fromCity,e.toCity)
            if dist < minDist:
                minDist = dist
                i = count 
            count += 1
        edges.insert(i,edge(edges[i].toCity,city)) 
        edges[i+1] = edge(city,edges[i+1].fromCity)    
    out = []
    out.append(cities[0])
    for x in edges:
        out.append(x.fromCity)
    #plot city numbers based on x and y cords
    fig = pypl.figure()                   
    ax = fig.add_subplot(111)            
    for c in cities:
        ax.annotate('%d' % c.number, xy=(c.x, c.y), textcoords='data')

    nums = []
    dist = 0
    for y in out:
        nums.append(y.number)
    for x in edges:
        dist += calcDistance(x.fromCity,x.toCity)
    print("-------Path-------")
    print(nums)
    print("-------Distance-------")
    print(dist)
    formatAndShow(out)
    
    print("-------Time Elasped-------")
    print("{0} seconds".format(time.time() - timer))


if (__name__ == '__main__'):
    main(sys.argv)