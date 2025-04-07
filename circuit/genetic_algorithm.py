import random
from gene import Gate, Gene
from chromosome import Chromosome, TABLE_LENGTH, get_inputs
from function import Function
POPULATION_SIZE = 1000
ELITISM_RATE = 0.06
CROSSOVER_RATE = 0.05
MUTATION_RATE = 0.2

def initialization(function: Function):
    return [Chromosome(function) for _ in range(POPULATION_SIZE)]

def selection(population: list[Chromosome]):
    result = []
    elite_chromosomes = elites(population)
    result.extend(elite_chromosomes)
    for i in range(len(population) - len(elite_chromosomes)):
        first_sample = random.randint(0, POPULATION_SIZE - 1)
        second_sample = random.randint(0, POPULATION_SIZE - 1)
        better_sample = max([population[first_sample], population[second_sample]], key=lambda ch: ch.score)
        result.append(better_sample)
    return result


def elites(population: list[Chromosome]) -> list[Chromosome]:
    cop = population.copy()
    cop.sort(reverse=True, key=lambda ch: ch.score)
    return cop[:int(POPULATION_SIZE * ELITISM_RATE)]




def rec_mutate(population: list[Chromosome], ind_gene: int, index: int, time: int):
    if ind_gene < TABLE_LENGTH ** 2:
        row = ind_gene // TABLE_LENGTH
        col = ind_gene % TABLE_LENGTH
        if row == 0:
            population[index].table[row, col] = Gene(get_inputs(population[index].table[row, col].wire1),
                                                     get_inputs(population[index].table[row, col].wire2),
                                                     random.choice(list(Gate)),
                                                     population[index].table[row, col].wire1, population[index].table[row, col].wire2,
                                                     col)
        else:
            population[index].table[row, col] = Gene(population[index].table[row - 1, population[index].table[row, col].wire1].outputs,
                                                     population[index].table[row - 1, population[index].table[row, col].wire2].outputs,
                                                     random.choice(list(Gate)),
                                                     population[index].table[row, col].wire1, population[index].table[row, col].wire2,
                                                     col)
        if row < TABLE_LENGTH - 1:
            for gene in population[index].table[row + 1]:
                if gene.wire1 == col or gene.wire2 == col:
                    rec_mutate(population, (row + 1) * TABLE_LENGTH + gene.wire_out, index, time + 1)
                    return
        else:
            rec_mutate(population, TABLE_LENGTH ** 2, index, time + 1)
            return
    else:
        if time == 0:
            population[index].last_gene = Gene(
                population[index].table[TABLE_LENGTH - 1, population[index].last_gene.wire1].outputs,
                population[index].table[TABLE_LENGTH - 1, population[index].last_gene.wire2].outputs,
                random.choice(list(Gate)),
                population[index].last_gene.wire1, population[index].last_gene.wire2,
                0)
        else:
            population[index].last_gene = Gene(
                population[index].table[TABLE_LENGTH - 1, population[index].last_gene.wire1].outputs,
                population[index].table[TABLE_LENGTH - 1, population[index].last_gene.wire2].outputs,
                population[index].last_gene.gate,
                population[index].last_gene.wire1, population[index].last_gene.wire2,
                0)





def mutate(population: list[Chromosome], function: Function):
    indices = random.choices(range(len(population)), k=int(len(population) * MUTATION_RATE))
    ind_gene = random.randint(0, 16)
    for index in indices:
        rec_mutate(population, ind_gene, index, 0)
        population[index].update_score(function)









