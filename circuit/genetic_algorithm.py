import random

import chromosome
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
    cop.sort(reverse=True, key=lambda ch: ch.score)
    return cop[:int(POPULATION_SIZE * ELITISM_RATE)]


def rec_mutate(population: list[Chromosome], row: int, col: int, ind: int, this_gene: Gene):
    if row != 0:
        new_gene = Gene(population[ind].table[row - 1, this_gene.wire1].outputs,
                        population[ind].table[row - 1, this_gene.wire2].outputs,
                        random.choice(list(Gate)),
                        this_gene.wire1, this_gene.wire2,
                        col)
    else:
        new_gene = Gene(chromosome.get_inputs(this_gene.wire1),
                        chromosome.get_inputs(this_gene.wire2),
                        random.choice(list(Gate)),
                        this_gene.wire1, this_gene.wire2,
                        col)
    population[ind].table[row, col] = new_gene
    if row != TABLE_LENGTH - 1:
        for i in range(TABLE_LENGTH):
            if population[ind].table[row + 1, i].wire1 == col or population[ind].table[row + 1, i].wire2 == col:
                rec_mutate(population, row + 1, i, ind, new_gene)
    else:
        if population[ind].last_gene.wire1 == new_gene.wire_out:
            population[ind].last_gene = Gene(new_gene.outputs,
                                             population[ind].last_gene.input2,
                                             population[ind].last_gene.gate,
                                             new_gene.wire_out, population[ind].last_gene.wire2,
                                             0)
        elif population[ind].last_gene.wire2 == new_gene.wire_out:
            population[ind].last_gene = Gene(population[ind].last_gene.input1,
                                             new_gene.outputs,
                                             population[ind].last_gene.gate,
                                             population[ind].last_gene.wire1, new_gene.wire_out,
                                             0)

def mutate(population: list[Chromosome], function: Function):
    chromosomes = random.choices(range(len(population)), k=int(len(population) * MUTATION_RATE))
    for i in chromosomes:
        num = random.randint(0, 16)
        if num == 16:
            population[i].last_gene = Gene(population[i].last_gene.input1,
                                           population[i].last_gene.input2,
                                           random.choice(list(Gate)),
                                           population[i].last_gene.wire1, population[i].last_gene.wire2,
                                           0)

        else:
            row = num // TABLE_LENGTH
            col = num % TABLE_LENGTH
            rec_mutate(population, row, col, i, population[i].table[row, col])
            population[i].update_score(function)









