import sys
import math
import random
import operator
from itertools import permutations 
import matplotlib.pyplot as pypl
import time

cities = []
distOverTime = []
minDist = []


class city:
    def __init__(self, number, x, y):
        self.number = number
        self.x = x
        self.y = y
    def distTo(self,city):
        calcDistance(city,self)
        
class Fitness:
    def __init__(self,path):
        self.path = path
        self.dist = 0
        self.fitnessNum = 0
    def getDist(self):
        pathDist = 0
        if len(self.path) == 0:
            return
        for i in range(0, len(self.path)):
            fromCity = self.path[i]
            if i + 1 < len(self.path):
                toCity = self.path[i + 1]
            else:
                toCity = self.path[0]
            pathDist += calcDistance(fromCity,toCity)
        self.dist = pathDist
        return self.dist
    def getFitness(self):
        self.fitnessNum = 1/float(self.getDist())
        return self.fitnessNum

def createPath(cities): #start with making a randomize path
    path = random.sample(cities,len(cities))
    return path

def initPopulation(cities):
    pop = []

    for x in range(0,len(cities)):
        pop.append(createPath(cities)) #Creates a population of 100 paths
    #print("initPop:{0}".format(len(pop)))
    return pop

def initAndRankFitness(population):
    allFitness = []
    for x in population: #for every item (path), made a fitness object out of it, stored in list
        allFitness.append(Fitness(x))
    allFitness.sort(key = (lambda fit:fit.getDist()), reverse=False) #sorts the fitness list by fitness score

    return allFitness


def selectBest(fitness): #Tournament sorting: select 10 random from fitness, 
    potentialParents = []
    #random.shuffle(fitness) #shuffle
    for i in range(0,len(fitness)/4): #takes the first 25
        potentialParents.append(fitness[i])
    potentialParents.sort(key =(lambda parent:parent.getDist())) #sort those 25 by fitnessNum
    #print("best:{0}".format(len(potentialParents)))
    return potentialParents #return the best Fitness, which is the first

def breed(p1,p2):
    cR = []
    c1 = []
    c2 = []

    g1 = int(random.randrange(0,100))
    g2 = int(random.randrange(0,100))

    minG = min(g1,g2)
    maxG = max(g1,g2)

    for x in range(minG,maxG):
        c1.append(p1[x])

    c2 = [city for city in p2 if city not in c1]

    cR = c1+c2
    return cR


def breedPopulation(bestSelected,genNum):
    bredPop = []
    for x in range(0,100):
        child = breed(random.choice(bestSelected).path,random.choice(bestSelected).path)
        while(Fitness(child).getDist() > distOverTime[genNum-1] or child == None):
            child = breed(random.choice(bestSelected).path,random.choice(bestSelected).path)
        bredPop.append(child)
    
    return bredPop

def mutate(path, mutRate):
    for x in range(0,len(path)):
        if(random.random() < mutRate):
            y = int(random.random() * len(path))

            c1 = path[x]
            c2 = path[y]
            path[x] = c2
            path[y] = c1
    return path


def mutatePop(pop,mutRate):
    mutatedPopulation = []
    for x in pop:
        mutated = mutate(x,mutRate)
        mutatedPopulation.append(mutated)
    return mutatedPopulation

def generations(currentGen,mutRate,genNum):
    sortedPaths = initAndRankFitness(currentGen)
    best = selectBest(sortedPaths)
    distOverTime.append(best[0].getDist())
    print(best[0].getDist())
    bredPop = breedPopulation(best,genNum)
    mutatePop = bredPop
    return mutatePop



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
    pypl.show()

def main(argv):
    timer = time.time()
    if (len(argv) < 3):
        print("No file name inputted or number of generations not inputted") #Error handling
        sys.exit(1)
    parseFile(argv[1]) #Parse file based on file name provided
    numberOfGens = int(argv[2])

    population = initPopulation(cities)
    fitness = Fitness(cities)
    print("Dist: {0}\tFitness: {1}".format(fitness.getDist(),float(fitness.getFitness())))
    distOverTime.append(fitness.getDist())
    

    for x in range(0,numberOfGens):
        print("gen: {0}".format(x+1))
        population = generations(population,.1,x)
    


    print("-------------------FINAL PATH---------------------")

    #plot city numbers based on x and y cords
    fig = pypl.figure()                   
    ax = fig.add_subplot(111)            
    for c in cities:
        ax.annotate('%d' % c.number, xy=(c.x, c.y), textcoords='data')

    sortedPath = initAndRankFitness(population)
    out = []
    for x in sortedPath[0].path:
         out.append(x.number)
    
    print("-------Path-------")
    print(out)

    print("-------Distance-------")
    print(distOverTime[int(len(distOverTime)-1)])

    formatAndShow(sortedPath[0].path)
    #pypl.clf()


    pypl.plot(distOverTime,marker ='o')
    pypl.show()

    
    print("-------Time Elasped-------")
    print("{0} seconds".format(time.time() - timer))


if (__name__ == '__main__'):
    main(sys.argv)