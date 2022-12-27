import csv
import pandas as pd
import random
import numpy
import time

# Global variables
data = pd.read_csv('LakeFishData.csv')
mileageLimit = 1000
fitnessScores = []
# Create a random genome (bitset of lakes, 1=visited, 0=not visited)
def createGenome():
    # Get length of data
    genomeLength = len(data)
    genome = []
    for i in range(genomeLength):
        genome.append(random.randint(0, 1))
    return genome

# Create a population of genomes
def createPopulation(populationSize):
    population = []
    for i in range(populationSize):
        population.append(createGenome())
    return population

# Fitness function for a genome. Higher # of fish = higher fitness
# If mileageLimit exceeded, return low fitness score of 0
def fitness_function(genome, data, mileageLimit):
    if(len(genome) != len(data)):
        print("Genome length not equal to data length")
        return 0
    mileage = 0
    fishCaught = 0

    # make list of distances and fish caught
    distances = data["Distance"].tolist()
    fish = data['Total Fish LB'].tolist()
    # sum the fish caught and mileage efficiently
    mileage = sum([distances[i] for i in range(len(genome)) if genome[i] == 1])
    fishCaught = sum([fish[i] for i in range(len(genome)) if genome[i] == 1])

    if(mileage > mileageLimit):
        return 0
    else:
        return fishCaught

# https://www.researchgate.net/publication/259461147_Selection_Methods_for_Genetic_Algorithms
# https://www.sciencedirect.com/topics/computer-science/wheel-selection
# Use a proportional selection method
# Maintains genetic diversity, prevents GA from converging to local optima
# Will use a roulette wheel selection method
def selection(population):
    fitnessScores.clear()
    fitnessScoresProbability = []
    totalFitnessScores = 0
    
    for genome in population:
        fitnessScores.append(fitness_function(genome, data, mileageLimit))

    totalFitnessScores = sum(fitnessScores)

    # Calculate probability of each genome being selected
    fitnessScoresProbability = [x / totalFitnessScores for x in fitnessScores]

    # Select two most fit individuals
    # https://stackoverflow.com/questions/3679694/a-weighted-version-of-random-choice
    individuals = numpy.random.choice(
        len(population), 2, p=fitnessScoresProbability)
    # Return the two genomes
    individual1 = population[individuals[0]]
    individual2 = population[individuals[1]]
    return [individual1, individual2]


# Crossover the two parent genomes using double point crossover
# https://ictactjournals.in/paper/IJSC_V6_I1_paper_4_pp_1083_1092.pdf,
# https://pubmed.ncbi.nlm.nih.gov/30055532/
def crossover(parent1, parent2):
    point1 = random.randint(0, len(parent1) - 1)
    point2 = random.randint(0, len(parent1) - 1)
    # check if identical crossover points
    while(point1 == point2):
        point2 = random.randint(0, len(parent1) - 1)
    if(point1 > point2):
        temp = point1
        point1 = point2
        point2 = temp
    offspring1 = parent1[:point1] + parent2[point1:point2] + parent1[point2:]
    offspring2 = parent2[:point1] + parent1[point1:point2] + parent2[point2:]
    return [offspring1, offspring2]

# Mutate the genome with a 1% chance
def mutate(genome):

    # mutate genome with 1% chance
    for i in range(len(genome)):
        if random.random() < 0.01:
            if(genome[i] == 1):
                genome[i] = 0
            else:
                genome[i] = 1
    return genome

def main():
    start = time.time()
    population = createPopulation(populationLimit)
    for i in range(generationLimit):
        parents = selection(population)
        offspring = crossover(parents[0], parents[1])
        offspring[0] = mutate(offspring[0])
        offspring[1] = mutate(offspring[1])
        population.append(offspring[0])  # add offspring to population and remove 2 lowest fitness
        population.append(offspring[1])
        fitnessScores.append(fitness_function(offspring[0], data, mileageLimit))
        fitnessScores.append(fitness_function(offspring[1], data, mileageLimit))
        zipped = zip(fitnessScores, population)
        sortedZipped = sorted(zipped, reverse=True)
        population = [element for _, element in sortedZipped]
        population = population[:populationLimit]
    end = time.time()
    
    with open('finalTimings.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([populationLimit, generationLimit, end - start, fitness_function(population[0], data, mileageLimit)])

if __name__ == '__main__':
    # Run main function with different population sizes and generation limits and record time
    with open('finalTimings.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Population Size", "Generation Limit", "Time", "Fitness Score"])
    populationLimits = [500, 1000, 1500, 2000, 2500]
    generationLimits = [500, 1000, 1500, 2000, 2500]
    for populationLimit in populationLimits:
        for generationLimit in generationLimits:
            populationLimit = populationLimit
            generationLimit = generationLimit
            main()