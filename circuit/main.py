import chromosome
from function import Function
import genetic_algorithm
from genetic_algorithm import initialization
GENERATIONS_COUNT = 200

if __name__ == '__main__':
    function = Function()
    f = open('answer.txt', 'w')
    f.write('')
    f.close()
    init_population = initialization(function)
    final_answer = None
    for i in range(GENERATIONS_COUNT):
        selected = genetic_algorithm.selection(init_population)
        selected[0].write_to_file(i)
        genetic_algorithm.crossover(selected, function)
        genetic_algorithm.mutate(selected, function)
        init_population = selected
        final_answer = selected[0]

