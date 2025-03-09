import numpy as np
import random

# Parameters
POP_SIZE = 50
CHROMO_LENGTH = 10  # Number of bits per chromosome
MUTATION_RATE = 0.1
CROSSOVER_RATE = 0.2
ELITISM_FRAC = 0.1
GENERATIONS = 100


# Decode binary to real number in range [0, 2pi]
def decode(chromosome):
    decimal_value = int("".join(map(str, chromosome)), 2)
    return (decimal_value / (2 ** CHROMO_LENGTH - 1)) * (2 * np.pi)


# Fitness function
def fitness(x):
    return np.sin(x)


# Initialize population
def init_population():
    return [random.choices([0, 1], k=CHROMO_LENGTH) for _ in range(POP_SIZE)]


# Tournament selection
def tournament_selection(pop, fitness_values, k=3):
    selected = random.sample(range(POP_SIZE), k)
    best = max(selected, key=lambda i: fitness_values[i])
    return pop[best]


# Crossover (random gene swap)
def crossover(parent1, parent2):
    if random.random() < CROSSOVER_RATE:
        child1, child2 = parent1[:], parent2[:]
        for i in range(CHROMO_LENGTH):
            if random.random() < 0.5:  # 50% chance to swap each gene
                child1[i], child2[i] = child2[i], child1[i]
        return child1, child2
    return parent1, parent2


# Mutation (randomly pick ONE index and flip it)
def mutate(chromosome):
    return [gene if random.random() > MUTATION_RATE else 1 - gene for gene in chromosome]


# Genetic Algorithm
def genetic_algorithm():
    population = init_population()
    num_elites = int(ELITISM_FRAC * POP_SIZE)

    for gen in range(GENERATIONS):
        decoded_values = np.array([decode(chromo) for chromo in population])
        fitness_values = np.array([fitness(x) for x in decoded_values])

        # Sort population by fitness (elitism)
        sorted_indices = np.argsort(fitness_values)[::-1]
        sorted_population = [population[i] for i in sorted_indices]

        # Keep elites
        new_population = sorted_population[:num_elites]

        # Select the rest from previous population via tournament selection
        while len(new_population) < POP_SIZE:
            p1 = tournament_selection(population, fitness_values)
            p2 = tournament_selection(population, fitness_values)

            offspring1, offspring2 = crossover(p1, p2)

            new_population.append(mutate(offspring1))
            if len(new_population) < POP_SIZE:
                new_population.append(mutate(offspring2))

        population = new_population

        # Print best solution per generation
        best_x = decode(population[0])
        print(f"Generation {gen + 1}: Best x = {best_x:.4f}, sin(x) = {np.sin(best_x):.4f}")

    return decode(population[0])


best_x = genetic_algorithm()
print(f"Optimal x: {best_x:.4f}, sin(x) = {np.sin(best_x):.4f}")
