import chromosome
from function import Function
import genetic_algorithm
from genetic_algorithm import initialization
GENERATIONS_COUNT = 100

if __name__ == '__main__':
    function = Function()
    init_population = initialization(function)
    chromosome.write_to_file(init_population, 0)
    print('\n\n\n\n\n\n')
    for i in range(GENERATIONS_COUNT):
        selected = genetic_algorithm.selection(init_population)
        genetic_algorithm.mutate(selected)
        init_population = selected.copy()
        chromosome.write_to_file(selected, i)
