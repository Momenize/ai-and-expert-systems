import random
from gene import Gate, Gene
from chromosome import Chromosome, TABLE_LENGTH
from function import Function
POPULATION_SIZE = 1000
ELITISM_RATE = 0.06
CROSSOVER_RATE = 0.05
MUTATION_RATE = 0.1

def initialization(function: Function):
    return [Chromosome(function) for _ in range(POPULATION_SIZE)]

def selection(population: list[Chromosome]):
    result = []
    elite_chromosomes = elites(population)
    result.extend(elite_chromosomes)
    for i in range(len(population) - len(elite_chromosomes)):
        first_sample = random.randint(0, POPULATION_SIZE - 1)
        second_sample = random.randint(0, POPULATION_SIZE - 1)
        better_sample = max([population[first_sample], population[second_sample]], key=lambda chromosome: chromosome.score)
        result.append(better_sample)
    return result


def elites(population: list[Chromosome]) -> list[Chromosome]:
    cop = population.copy()
    cop.sort(reverse=True, key=lambda chromosome: chromosome.score)
    return cop[:int(POPULATION_SIZE * ELITISM_RATE)]

# def crossover(population: list[Chromosome]):
#     for i in range(int(len(population) * CROSSOVER_RATE)):
#         first_chromosome = random.randint(0, len(population) - 1)
#         second_chromosome = random.randint(0, len(population) - 1)
#         crosspoint = random.randint(0, TABLE_LENGTH ** 2 + 1)
#

def mutate(population: list[Chromosome]):
    for i in range(int(len(population) * MUTATION_RATE)):
        column = random.randint(0, 3)
        row = random.randint(0, 3)
        ind = random.randint(0, len(population) - 1)
        population[ind].table[column, row] = (
            Gene(
                population[ind].table[column, row].input1,
                population[ind].table[column, row].input2,
                random.choice(list(Gate))))


