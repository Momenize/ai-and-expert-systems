from function import Function
import genetic_algorithm
from genetic_algorithm import initialization
GENERATIONS_COUNT = 100

if __name__ == '__main__':
    function = Function()
    f = open('answer.txt', 'w')
    f.write('')
    f.close()
    init_population = initialization(function)
    selected = genetic_algorithm.selection(init_population)
    final_answer = None
    for i in range(GENERATIONS_COUNT):
        selected[0].write_to_file(i)
        genetic_algorithm.mutate(selected, function)
        genetic_algorithm.crossover(selected, function)
        final_answer = selected[0]
        selected = genetic_algorithm.selection(selected)

