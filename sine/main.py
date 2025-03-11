from operator import indexOf

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
    optimal_x = max(selected, key=lambda i: fitness_values[i])

    return pop[optimal_x]


# Crossover (randomly pick 20% of population and swap a random segment)
def crossover(population):
    num_crossovers = int(CROSSOVER_RATE * POP_SIZE)
    selected_indices = random.sample(range(POP_SIZE), num_crossovers)
    random.shuffle(selected_indices)  # Shuffle to ensure random pairs

    for i in range(0, len(selected_indices) - 1, 2):
        p1, p2 = selected_indices[i], selected_indices[i + 1]

        # Choose two random crossover points
        start, end = sorted(random.sample(range(CHROMO_LENGTH), 2))

        # Swap the bits between the indices
        population[p1][start:end], population[p2][start:end] = (
            population[p2][start:end], population[p1][start:end]
        )

    return population


# Mutation (generate one random index and flip it for each randomly selected chromosome)
def mutate(population):
    num_mutations = int(MUTATION_RATE * len(population))
    selected_indices = random.sample(range(len(population)), num_mutations)
    mutation_index = random.randint(0, CHROMO_LENGTH - 1)  # Generate a single random index

    for i in selected_indices:
        population[i][mutation_index] = 1 - population[i][mutation_index]  # Flip bit at the generated index

    return population


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

            new_population.append(p1[:])
            if len(new_population) < POP_SIZE:
                new_population.append(p2[:])

        # Apply crossover
        new_population = crossover(new_population)

        # Apply mutation
        new_population = mutate(new_population)

        population = new_population

        # Print best solution per generation
        x = decode(population[0])
        print(f"Generation {gen + 1}: Best x = {x:.4f}, sin(x) = {np.sin(x):.4f}")

    return decode(population[0])


best = genetic_algorithm()
print(f"Optimal x: {best:.4f}, sin(x) = {np.sin(best):.4f}")
