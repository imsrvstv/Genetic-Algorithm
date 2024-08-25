import random
import copy
from tabulate import tabulate


class Individual:
    def __init__(self, size: int) -> None:
        self.size = size
        self.chromosome = []
        self.fitness = 0.0

    def generateChromosome(self) -> None:
        for _ in range(self.size):
            self.chromosome.append(self.generateGene())

    def generateGene(self) -> int:
        return random.randint(0, 1)


def fitness(ind: Individual, items: list, capacity: int) -> None:
    totalPrice = 0
    totalWeight = 0

    for i in range(ind.size):
        if ind.chromosome[i] == 1:
            totalPrice += items[i]["price"]
            totalWeight += items[i]["weight"]

    fitness = totalPrice
    if totalWeight > capacity:
        fitness = -1
    ind.fitness = fitness


def selection(population: list) -> Individual:
    k = 5
    bestIndividual = copy.deepcopy(population[0])

    for _ in range(k):
        choice = random.randint(0, len(population) - 1)
        if population[choice].fitness > bestIndividual.fitness:
            bestIndividual = copy.deepcopy(population[choice])

    return bestIndividual


def crossover(parent1: Individual, parent2: Individual) -> Individual:
    child = Individual(parent1.size)
    crossoverRate = 0.5

    child.chromosome = (
        parent1.chromosome[0 : int(parent1.size * crossoverRate)]
        + parent2.chromosome[int(parent2.size * crossoverRate) :]
    )

    return child


def mutation(child: Individual) -> None:
    mutationRate = 0.05

    for i in range(child.size):
        if random.random() < mutationRate:
            child.chromosome[i] = (child.chromosome[i] + 1) % 2


class Population:
    def __init__(self, size: int, items: list, capacity: int) -> None:
        self.size = size
        self.population = []
        self.items = items
        self.capacity = capacity

    def generatePopulation(self) -> None:
        for _ in range(self.size):
            ind = Individual(len(self.items))
            ind.generateChromosome()
            self.population.append(ind)

    def evolve(self, generations: int) -> list:
        populationLog = [["Generation", "Best Fitness", "Average Fitness"]]

        for i in range(generations):
            bestFitness = 0.0
            avgFitness = 0.0
            for ind in self.population:
                fitness(ind, self.items, self.capacity)
                if ind.fitness > bestFitness:
                    bestFitness = ind.fitness
                avgFitness += ind.fitness
            avgFitness = avgFitness / self.size

            if i == 0 or (i + 1) % 10 == 0:
                populationLog.append([str(i + 1), str(bestFitness), str(avgFitness)])

            newPopulation = []

            for j in range(self.size):
                parent1 = selection(self.population)
                parent2 = selection(self.population)
                child = crossover(parent1, parent2)
                mutation(child)
                newPopulation.append(child)

            self.population = newPopulation

        return populationLog


def main(size: int, items: list, capacity: int) -> None:
    pop = Population(size, items, capacity)
    pop.generatePopulation()

    # Comment below 2 LOC for results without evolution
    populationLog = pop.evolve(100)
    print(tabulate(populationLog, headers="firstrow"), end="\n\n")

    bestIndividual = copy.deepcopy(pop.population[0])
    for ind in pop.population:
        fitness(ind, items, capacity)
        if ind.fitness > bestIndividual.fitness:
            bestIndividual = copy.deepcopy(ind)

    result = [["Item", "Price", "Weight"]]
    totalWeight = 0

    for i in range(bestIndividual.size):
        if bestIndividual.chromosome[i] == 1:
            result.append([items[i]["name"], items[i]["price"], items[i]["weight"]])
            totalWeight += items[i]["weight"]

    print(tabulate(result, headers="firstrow"), end="\n\n")
    print(f"Total Price: {bestIndividual.fitness}")
    print(f"Total Weight: {totalWeight}")


ITEMS = [
    {"name": "Clay Pot", "weight": 20, "price": 30},
    {"name": "Tooth Pick", "weight": 1, "price": 3},
    {"name": "Mouse Pad", "weight": 4, "price": 50},
    {"name": "Canvas", "weight": 10, "price": 40},
    {"name": "Pencil", "weight": 2, "price": 4},
    {"name": "Mirror", "weight": 10, "price": 30},
    {"name": "Eraser", "weight": 2, "price": 3},
    {"name": "Bottle Cap", "weight": 1, "price": 1},
    {"name": "Rusty Nail", "weight": 5, "price": 1},
    {"name": "Peanuts", "weight": 6, "price": 10},
]
WEIGHT_CAPACITY = 30
POPULATION_SIZE = 10


main(POPULATION_SIZE, ITEMS, WEIGHT_CAPACITY)
