import random
import numpy as np
from gene import Gene, Gate, INPUTS_COUNT
from function import Function
TABLE_LENGTH = 4
class Chromosome:
    def __init__(self, function: Function):
        self.table = np.empty(shape=(TABLE_LENGTH, TABLE_LENGTH), dtype=Gene)
        for i in range(TABLE_LENGTH):
            input_1 = get_inputs(random.choice([0, 1, 2, 3]))
            input_2 = get_inputs(random.choice([0, 1, 2, 3]))
            self.table[0, i] = Gene(input_1, input_2, random.choice(list(Gate)))
        for i in range(1, TABLE_LENGTH):
            for j in range(0, TABLE_LENGTH):
                input_1 = random.choice([self.table[i - 1, k] for k in range(TABLE_LENGTH)]).outputs
                input_2 = random.choice([self.table[i - 1, k] for k in range(TABLE_LENGTH)]).outputs
                self.table[i, j] = Gene(input_1, input_2, random.choice(list(Gate)))
        self.last_gene = Gene(
            random.choice(self.table[3]).outputs,
            random.choice(self.table[3]).outputs,
            random.choice(list(Gate))
        )
        match_counts = 0
        for i in range(len(self.last_gene.outputs)):
            if self.last_gene.outputs[i] == bool(function.terms[i]):
                match_counts += 1
        self.score = match_counts * 100 / len(self.last_gene.outputs)




def get_inputs(val):
    inputs = [f'{i:04b}' for i in range(TABLE_LENGTH ** 2)]
    res = []
    for string in inputs:
        res.append(string[3 - val])
    return res


def write_to_file(ch_list: list[Chromosome], generation: int):
    f = open("answer.txt", "a")
    f.write('Generation ' f'{generation}:\n\n')
    for inp in range(INPUTS_COUNT ** 2):
        text = f'{inp:04b}', ': ', f'{ch_list[0].last_gene.outputs[inp]}'
        string_text = ' '.join(text)
        f.write(string_text)
        f.write('\n----------------------------------\n\n\n')
    f.write(f'\nScore: {ch_list[0].score}')