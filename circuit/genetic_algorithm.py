import random
from gene import Gate, Gene
from chromosome import Chromosome, TABLE_LENGTH, get_inputs
from function import Function
POPULATION_SIZE = 500
ELITISM_RATE = 0.1
CROSSOVER_RATE = 0.3
MUTATION_RATE = 0.3

def initialization(function: Function):
    return [Chromosome(function) for _ in range(POPULATION_SIZE)]

def selection(population: list[Chromosome]):
    elite_chromosomes = elites(population)
    result = []
    result.extend(reversed(elite_chromosomes))
    for i in range(len(population) - int(len(population) * ELITISM_RATE)):
        first_sample = random.randint(int(POPULATION_SIZE * ELITISM_RATE), POPULATION_SIZE - 1)
        second_sample = random.randint(int(POPULATION_SIZE * ELITISM_RATE), POPULATION_SIZE - 1)
        better_sample = max([population[first_sample], population[second_sample]], key=lambda ch: ch.score)
        result.append(better_sample)
    return result


def elites(population: list[Chromosome]) -> list[Chromosome]:
    cop = population.copy()
    cop.sort(key=lambda ch: ch.score)
    return cop[-int(len(cop) * ELITISM_RATE):]







def mutate(population: list[Chromosome], function: Function):
    indices = random.choices(range(int(len(population) * ELITISM_RATE), len(population)), k=int(len(population) * MUTATION_RATE))
    for index in indices:
        num_gene = random.randint(0, 15)
        row = num_gene // TABLE_LENGTH
        col = num_gene % TABLE_LENGTH
        if row == 0:
            wire1 = random.randint(0, TABLE_LENGTH - 1)
            wire2 = random.randint(0, TABLE_LENGTH - 1)
            population[index].table[row, col] = Gene(get_inputs(wire1),
                                                     get_inputs(wire2),
                                                     random.choice(list(Gate)),
                                                     wire1, wire2, col)
            population[index].refresh(row)
            population[index].update_score(function)
        else:
            wire1 = random.randint(0, TABLE_LENGTH - 1)
            wire2 = random.randint(0, TABLE_LENGTH - 1)
            population[index].table[row, col] = Gene(population[index].table[row - 1, wire1].outputs,
                                                     population[index].table[row - 1, wire2].outputs,
                                                     random.choice(list(Gate)),
                                                     wire1, wire2, col)
            population[index].refresh(row)
            population[index].update_score(function)





def crossover(population: list[Chromosome], function: Function):
    indices = random.choices(range(int(len(population) * ELITISM_RATE), len(population)), k=int(len(population) * CROSSOVER_RATE))

    for index in indices:
        row0 = random.randint(0, TABLE_LENGTH - 1)
        col0 = random.randint(0, TABLE_LENGTH - 1)
        second_index = random.choice(indices)
        for i in range(2):
            if row0 == 0:
                first_gene = population[index].table[row0, col0]
                population[index].table[row0, col0] = Gene(get_inputs(population[second_index].table[row0, col0].wire1),
                                                           get_inputs(population[second_index].table[row0, col0].wire2),
                                                                      population[second_index].table[row0, col0].gate,
                                                                      population[second_index].table[row0, col0].wire1,
                                                           population[second_index].table[row0, col0].wire2,
                                                           col0)
                population[second_index].table[row0, col0] = Gene(get_inputs(first_gene.wire1),
                                                                  get_inputs(first_gene.wire2),
                                                                  first_gene.gate,
                                                                  first_gene.wire1, first_gene.wire2,
                                                                  col0)
                population[index].refresh(row0)
                population[second_index].refresh(row0)
                population[index].update_score(function)
                population[second_index].update_score(function)
            else:
                first_gene = population[index].table[row0, col0]
                population[index].table[row0, col0] = Gene(population[index].table[row0 - 1, population[second_index].table[row0, col0].wire1].outputs,
                                                           population[index].table[row0 - 1, population[second_index].table[row0, col0].wire2].outputs,
                                                           population[second_index].table[row0, col0].gate,
                                                           population[second_index].table[row0, col0].wire1,
                                                           population[second_index].table[row0, col0].wire2,
                                                           col0)
                population[second_index].table[row0, col0] = Gene(population[second_index].table[row0 - 1, first_gene.wire1].outputs,
                                                                  population[second_index].table[row0 - 1, first_gene.wire2].outputs,
                                                                  first_gene.gate,
                                                                  first_gene.wire1, first_gene.wire2,
                                                                  col0)
                population[index].refresh(row0)
                population[index].update_score(function)
                population[second_index].refresh(row0)
                population[second_index].update_score(function)






# def rec_mutate(population: list[Chromosome], num_gene: int, index: int, time: int):
#     if num_gene < TABLE_LENGTH ** 2:
#         row = num_gene // TABLE_LENGTH
#         col = num_gene % TABLE_LENGTH
#         if row == 0:
#             new_input0 = new_input1 = random.randint(0, TABLE_LENGTH - 1)
#             population[index].table[row, col] = Gene(get_inputs(new_input0),
#                                                      get_inputs(new_input1),
#                                                      random.choice(list(Gate)),
#                                                      new_input0, new_input1,
#                                                      col)
#         else:
#             if time > 0:
#                 population[index].table[row, col] = Gene(population[index].table[row - 1, population[index].table[row, col].wire1].outputs,
#                                                          population[index].table[row - 1, population[index].table[row, col].wire2].outputs,
#                                                          population[index].table[row, col].gate,
#                                                          population[index].table[row, col].wire1, population[index].table[row, col].wire2,
#                                                          col)
#             else:
#                 new_input0 = new_input1 = random.randint(0, TABLE_LENGTH - 1)
#                 population[index].table[row, col] = Gene(population[index].table[row - 1, new_input0].outputs,
#                                                          population[index].table[row - 1, new_input1].outputs,
#                                                          random.choice(list(Gate)),
#                                                          new_input0, new_input1, col)
#         if row < TABLE_LENGTH - 1:
#             for gene in population[index].table[row + 1]:
#                 if gene.wire1 == col or gene.wire2 == col:
#                     rec_mutate(population, (row + 1) * TABLE_LENGTH + gene.wire_out, index, time + 1)
#                     return
#         else:
#             rec_mutate(population, TABLE_LENGTH ** 2, index, time + 1)
#             return
#     else:
#         if time == 0:
#             population[index].last_gene = random.choice(population[index].table[TABLE_LENGTH - 1])
#         else:
#             population[index].last_gene = population[index].table[TABLE_LENGTH - 1, population[index].last_gene.wire_out]


