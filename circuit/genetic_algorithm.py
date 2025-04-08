import random
from gene import Gate, Gene
from chromosome import Chromosome, TABLE_LENGTH, get_inputs
from function import Function
POPULATION_SIZE = 1000
ELITISM_RATE = 0.1
CROSSOVER_RATE = 0.2
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




def rec_mutate(population: list[Chromosome], num_gene: int, index: int, time: int):
    if num_gene < TABLE_LENGTH ** 2:
        row = num_gene // TABLE_LENGTH
        col = num_gene % TABLE_LENGTH
        if row == 0:
            new_input0 = new_input1 = random.randint(0, TABLE_LENGTH - 1)
            population[index].table[row, col] = Gene(get_inputs(new_input0),
                                                     get_inputs(new_input1),
                                                     random.choice(list(Gate)),
                                                     new_input0, new_input1,
                                                     col)
        else:
            if time > 0:
                population[index].table[row, col] = Gene(population[index].table[row - 1, population[index].table[row, col].wire1].outputs,
                                                         population[index].table[row - 1, population[index].table[row, col].wire2].outputs,
                                                         population[index].table[row, col].gate,
                                                         population[index].table[row, col].wire1, population[index].table[row, col].wire2,
                                                         col)
            else:
                new_input0 = new_input1 = random.randint(0, TABLE_LENGTH - 1)
                population[index].table[row, col] = Gene(population[index].table[row - 1, new_input0].outputs,
                                                         population[index].table[row - 1, new_input1].outputs,
                                                         random.choice(list(Gate)),
                                                         new_input0, new_input1, col)
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
            population[index].last_gene = random.choice(population[index].table[TABLE_LENGTH - 1])
        else:
            population[index].last_gene = population[index].table[TABLE_LENGTH - 1, population[index].last_gene.wire_out]





def mutate(population: list[Chromosome], function: Function):
    indices = random.choices(range(len(population)), k=int(len(population) * MUTATION_RATE))
    num_gene = random.randint(0, 16)
    for index in indices:
        rec_mutate(population, num_gene, index, 0)
        population[index].update_score(function)

def crossover(population: list[Chromosome], function: Function):
    indices = random.choices(range(len(population)), k=int(len(population) * CROSSOVER_RATE))
    for index in indices:
        next_index = random.choice(indices)
        first_last_row = population[index].table[TABLE_LENGTH - 1]
        for i in range(TABLE_LENGTH):
            population[index].table[TABLE_LENGTH - 1, i] = Gene(
                population[index].table[TABLE_LENGTH - 2, population[next_index].table[TABLE_LENGTH - 1, i].wire1].outputs,
                population[index].table[TABLE_LENGTH - 2, population[next_index].table[TABLE_LENGTH - 1, i].wire2].outputs,
                population[next_index].table[TABLE_LENGTH - 1, i].gate,
                population[next_index].table[TABLE_LENGTH - 1, i].wire1,
                population[next_index].table[TABLE_LENGTH - 1, i].wire2,
                i)
            population[next_index].table[TABLE_LENGTH - 1, i] = Gene(population[next_index].table[TABLE_LENGTH - 2, first_last_row[i].wire1].outputs,
                                                                     population[next_index].table[TABLE_LENGTH - 2, first_last_row[i].wire2].outputs,
                                                                     first_last_row[i].gate,
                                                                     first_last_row[i].wire1, first_last_row[i].wire2,
                                                                     TABLE_LENGTH - 1)
        population[index].last_gene = population[index].table[TABLE_LENGTH - 1, population[next_index].last_gene.wire_out]
        population[next_index].last_gene = population[next_index].table[TABLE_LENGTH - 1, population[index].last_gene.wire_out]
        population[index].update_score(function)
        population[next_index].update_score(function)
