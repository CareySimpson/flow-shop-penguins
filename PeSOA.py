# -*- coding: utf-8 -*-
'''
    Penguin Search Optimization Algorithm for the Flow-Shop Scheduling Problem
'''
#imports the random class
import random

#sets our maximum integer constant
MAX = 9223372036854775807

#Initializes number of penguins in our waddle, generations to test, 
#reserve oxygen (used in loops), and number of jobs and machines (n and m)
penguins = 10
waddle = []
generations = 100
oxygen = 10
n = int(random.random() * MAX % 10) + 1
m = int(random.random() * MAX % 10) + 1

#Penguin class that has a solution, best solution, and makespan. solution and best
#are permutations of the jobs and makespan is an integer representing the time for
#m machines to process n jobs in the order given by the solution list.
class Penguin():
    solution = []
    def __init__(self, solution, makespan):
        self.solution = solution
        self.best = self.solution
        self.makespan = makespan
        
    #ToString method for printing current solution and makespan.
    def __str__(self):
        return ("\nSolution: " + str(self.solution) + "\nMakespan: " + str(self.makespan) + "\n")
  
#Creates a list of n jobs, each with m tasks of random execution times
def createJobs(n):
    jobs = []
    for i in range(n):
        jobs.append([])
        for j in range(m):
            jobs[i].append(int(random.random() * MAX % 100)+1)
    return jobs

#Recursive method given by section 2.2 of the article that finds the makespan of the solution
def makespan(jobs, solution, j, k):
    if j == 0 and k == 0:
        return jobs[solution[j]][k]
    if j == 0:
        return makespan(jobs, solution, j, k-1) + jobs[solution[j]][k]
    if k == 0:
        return makespan(jobs, solution, j-1, k) + jobs[solution[j]][k]
    else:
        return max(makespan(jobs, solution, j-1, k), makespan(jobs, solution, j, k-1)) + jobs[solution[j]][k]
    
#Generates a randomly-ordered schedule of jobs
def randomSolution(n):
    #First gets an ordered sequence
    solution = []
    for i in range(n):
        solution.append(i)
        
    #Then jumbles the sequence up
    randomSolution = []
    while not len(solution) == 0:
        randomSolution.append(solution.pop(int(random.random() * MAX % len(solution))))
    return randomSolution

#The main part of the algorithm given by section 4.3 of the article.
def getNewSolution(p, b):
    #Local best, the penguin's current solution, an empty list Q, and a loop counter.
    best = b
    current = randomSolution(n)
    Q = []
    loop = oxygen
    
    #Equation 7: Snew = Sid + rand * (Sbest - Snew)
    while loop > 0:
        #Sbest - Sid = Q
        #Creates a list of tuples for swapping
        for i in range(len(current)):
            if(current[i] != best[i]):
                Q.append([current[i], best[i]])
        
        #rand * Q = Q'
        #Removes some items from Q
        r = int(random.random() * n)
        while Q != [] and r > 0:
            Q.pop(int(random.random() * len(Q)))
            r -= 1
         
        #Sid + Q' = Snew
        #Swaps positions of some items in current solution given by Q
        for i in range(len(Q)):
            temp = current[Q[i][0]]
            current[Q[i][0]] = current[Q[i][1]]
            current[Q[i][1]] = temp
        
        #If it's better, keep it, then loop again until counter goes to 0
        p.solution = current
        if(p.makespan > makespan(jobs, p.solution, n-1, m-1)):
            p.best = p.solution
        
        loop -= 1
    
print(penguins, "Penguins")
print("Number of jobs:", n)
print("Number of machines:", m ,"\n")

#Initialize jobs   
jobs = createJobs(n)

#Initialize our waddle of penguins
for i in range(penguins):
    randSolution = randomSolution(n)
    waddle.append(Penguin(randSolution, makespan(jobs, randSolution, n-1, m-1)))

#Initialize the best solution
bestSol = []
for i in range(n):
    bestSol.append(i)
bestSpan = makespan(jobs, bestSol, n-1, m-1)
    
#Tests each penguin for the specified number of generations
for g in range(generations):
    #First finds the makespan of all the penguins and keeps the best solution
    print("Generation", g, "\n")
    for p in waddle:
        if p.makespan < bestSpan:
            bestSol = p.solution
            bestSpan = p.makespan
            
    #Prints each penguin's info then gives it a new solution based on the current best solution.
    i = 1
    for p in waddle:
        print("Penguin", i, p)
        i += 1
        getNewSolution(p, bestSol)
        p.makespan = makespan(jobs, p.solution, n-1, m-1)

    print("Best makespan so far:", bestSpan, "\n")
