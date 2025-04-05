import random
from gene import Gate, Gene
from chromosome import Chromosome, TABLE_LENGTH
from function import Function
POPULATION_SIZE = 1000
ELITISM_RATE = 0.06
CROSSOVER_RATE = 0.05
MUTATION_RATE = 0.05

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


def rec_mutate(population: list[Chromosome], row: int, col: int, ind: int, this_gene: Gene):
    new_gene = Gene(this_gene.input1,
                    this_gene.input2,
                    random.choice(list(Gate)))
    if row != TABLE_LENGTH - 1:
        for i in range(TABLE_LENGTH):
            if (population[ind].table[row + 1, i].input1 == this_gene or
                    population[ind].table[row + 1, i].input2 == this_gene):
                rec_mutate(population, row + 1, i, ind, population[ind].table[row + 1, i])
    else:
        if population[ind].last_gene.input1 == this_gene:
            population[ind].last_gene = Gene(new_gene.outputs,
                                             population[ind].last_gene.input2,
                                             population[ind].last_gene.gate)
        elif population[ind].last_gene.input2 == this_gene:
            population[ind].last_gene = Gene(population[ind].last_gene.input1,
                                             new_gene.outputs,
                                             population[ind].last_gene.gate)
    population[ind].table[row, col] = new_gene
def mutate(population: list[Chromosome], function: Function):
    chromosomes = random.choices(range(len(population)), k=int(len(population) * MUTATION_RATE))
    for i in chromosomes:
        num = random.randint(0, 16)
        if num == 16:
            population[i].last_gene = Gene(population[i].last_gene.input1,
                                           population[i].last_gene.input2,
                                           random.choice(list(Gate)))

        else:
            row = num // TABLE_LENGTH
            col = num % TABLE_LENGTH
            rec_mutate(population, row, col, i, population[i].table[row, col])
            population[i].update_score(function)









