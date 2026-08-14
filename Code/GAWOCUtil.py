import numpy
import random


# Function to initialize a population
def initializepop(popsize, nlength):  # Function parameters establish number of pop. members & chromosome length
    population = []
    for i in range(popsize):
        chromosome = random.sample(range(1, nlength + 1), nlength)
        population.append(chromosome)
    return population


# Function to initialize a population
def reinitializepop(popsize, nlength,
                    bestpaths):  # Function parameters establish number of pop. members & chromosome length
    wocinsertions = int(popsize * 0.1)
    population = initializepop(popsize, nlength)
    for i in range(wocinsertions):
        if(len(bestpaths)>0):
            population[i] = bestpaths[random.randrange(len(bestpaths))]
    return population


def evalfitness(c, n):
    # threatlevel is my fitness. -1 each time a threatening queen is found.
    threatlevel = n
    fitness = 0.0
    for i in range(len(c) - 1):
        # Current queen being checked against all others
        Q1col = i
        Q1row = c[i]
        for j in range(i + 1, len(c)):  # Start from i + 1 to avoid checking the same pair twice
            # Possible enemy queen being checked
            Q2col = j
            Q2row = c[j]
            if (Q1col != Q2col and Q1row != Q2row) and (
                    abs(Q1col - Q2col) == abs(Q1row - Q2row) or Q1col == Q2col or Q1row == Q2row):
                threatlevel -= 1
    fitness = threatlevel / n
    return fitness


def newGen(population, mrate, n):
    fitList = []
    for i in population:
        fitList.append(evalfitness(i, n))

    newPopulation = []
    for count in range(len(population)):
        parent1 = population[pick_one(fitList)]
        parent2 = population[pick_one(fitList)]
        temp1, temp2 = crossovero1(parent1, parent2)
        mutate(temp1, mrate)
        mutate(temp2, mrate)
        newPopulation.append(random.choice([temp1, temp2]))
    return newPopulation


def pick_one(probabilities):
    # Generate a random value in the range [0, 1)
    random_value = random.random()

    # Initialize the cumulative probability
    cumulative_prob = 0.0

    for index, prob in enumerate(probabilities):
        cumulative_prob += prob
        if random_value < cumulative_prob:
            return index


def crossovero1(parent1, parent2):
    size = len(parent1)
    swappoints = sorted(random.sample(range(size), 2))
    child1 = [-1] * size
    child2 = [-1] * size

    for i in range(swappoints[0], swappoints[1]):
        child1[i] = parent1[i]
        child2[i] = parent2[i]
    indexc1 = 0
    indexc2 = 0

    for i in range(size):
        if parent2[i] not in child1:
            while child1[indexc1] != -1:
                indexc1 += 1
            child1[indexc1] = parent2[i]

        if parent1[i] not in child2:
            while child2[indexc2] != -1:
                indexc2 += 1
            child2[indexc2] = parent1[i]

    return child1, child2


def mutate(chromosome, mrate):  # Mutation method
    if random.random() < mrate:  # Determines to mutate or not based on passed mutation rate
        i, j = random.sample(range(len(chromosome)), 2)  # Get specific data within chromosome to swap
        chromosome[i], chromosome[j] = chromosome[j], chromosome[i]  # Swap two genes in the chromosome


def geneticalgorithmo1woc(n, woc, popsize, numgens, mrate):
    # Genetic algorithm using TWO point mutation

    population = initializepop(popsize, n)
    bestcombination = None
    bestdistance = float('-inf')
    bestcosts = []
    bestpaths = []  # New array to store best paths for each generation
    oppaths = []
    opcosts = []
    for WOCgeneration in range(woc):
        print("WOCgen", WOCgeneration)
        print("\n\nOp path: \n", WOCgeneration, bestpaths)
        if WOCgeneration != 0:
            population = reinitializepop(popsize, n, oppaths)
            for x in range(len(population)):
                print("WOCPOP:", population[x])
                fitscoreWOC = evalfitness(population[x], n)
                print(fitscoreWOC)
        for generation in range(numgens):
            fitscores = [evalfitness(chromosome, n) for
                         chromosome in population]

            # Include elitism: Select the best individual to preserve
            bestmember = numpy.argmax(fitscores)
            generationbestdistance = fitscores[bestmember]

            if generationbestdistance > bestdistance:
                bestcombination = population[bestmember]
                bestdistance = generationbestdistance

            opcosts.append(bestdistance)
            bestcosts.append(bestdistance)
            bestpaths.append(bestcombination)  # Store the best path for the current generation

            population = newGen(population, mrate, n)
            '''
            amtparents = int(0.2 * popsize)
            parents = [population[i] for i in numpy.argsort(fitscores)[:amtparents]]

            offspring = []
            while len(offspring) < popsize - amtparents:
                parent1, parent2 = random.choices(parents, k=2)
                child1, child2 = crossovero1(parent1, parent2)
                mutate(child1, mrate)
                mutate(child2, mrate)
                offspring.append(child1)
                offspring.append(child2)

            population = parents + offspring
            '''

            """print("\nGen", generation)
            for x in range(len(population)):
                print(x + 1, "member", population[x])
            """
            print("Best cost, ", bestdistance)
            print(bestcombination)
            # Check if the best fitness has reached 1
            if bestdistance == 1:
                break
        if bestdistance == 1:
            break
        oppaths.append(bestcombination)
    print("best comb:", bestcombination)
    return bestcombination, bestdistance, bestcosts, bestpaths


def geneticalgorithmo1(n, woc, popsize, numgens, mrate):
    # Genetic algorithm using TWO point mutation

    population = initializepop(popsize, n)
    bestcombination = None
    bestdistance = float('-inf')
    bestcosts = []
    bestpaths = []  # New array to store best paths for each generation

    for generation in range(numgens):
        fitscores = [evalfitness(chromosome, n) for
                          chromosome in population]

        # Include elitism: Select the best individual to preserve
        bestmember = numpy.argmax(fitscores)
        generationbestdistance = fitscores[bestmember]

        if generationbestdistance > bestdistance:
            bestcombination = population[bestmember]
            bestdistance = generationbestdistance

        bestcosts.append(bestdistance)
        bestpaths.append(bestcombination)  # Store the best path for the current generation

        population = newGen(population, mrate, n)
        '''
        amtparents = int(0.2 * popsize)
        parents = [population[i] for i in numpy.argsort(fitscores)[:amtparents]]

        offspring = []
        while len(offspring) < popsize - amtparents:
            parent1, parent2 = random.choices(parents, k=2)
            child1, child2 = crossovero1(parent1, parent2)
            mutate(child1, mrate)
            mutate(child2, mrate)
            offspring.append(child1)
            offspring.append(child2)

        population = parents + offspring
        '''

        print("\nGen", generation)
        for x in range(len(population)):
            print(x + 1, "member", population[x])

        # Check if the best fitness has reached 1
        if bestdistance == 1:
            break
    return bestcombination, bestdistance, bestcosts, bestpaths
