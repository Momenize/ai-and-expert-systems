import random
import numpy as np
from gene import Gene, Gate, INPUTS_COUNT
from function import Function
TABLE_LENGTH = 4
class Chromosome:
    def __init__(self, function: Function):
        self.table = np.empty(shape=(TABLE_LENGTH, TABLE_LENGTH), dtype=Gene)
        for i in range(TABLE_LENGTH):
            input_1 = random.choice([0, 1, 2, 3])
            input_2 = random.choice([0, 1, 2, 3])
            self.table[0, i] = Gene(get_inputs(input_1), get_inputs(input_2), random.choice(list(Gate)))
        for i in range(1, TABLE_LENGTH):
            for j in range(0, TABLE_LENGTH):
                input_1 = random.choice([self.table[i - 1, k] for k in range(TABLE_LENGTH)])
                input_2 = random.choice([self.table[i - 1, k] for k in range(TABLE_LENGTH)])
                self.table[i, j] = Gene(input_1.outputs, input_2.outputs, random.choice(list(Gate)))
        in1 = random.choice(self.table[3])
        in2 = random.choice(self.table[3])
        self.last_gene = Gene(
            in1.outputs, in2.outputs,
            random.choice(list(Gate))
        )
        match_counts = 0
        for i in range(len(self.last_gene.outputs)):
            if self.last_gene.outputs[i] == bool(function.terms[i]):
                match_counts += 1
        self.score = match_counts * 100 / len(self.last_gene.outputs)

    def update_score(self, function: Function):
        match_counts = 0
        for i in range(len(self.last_gene.outputs)):
            if self.last_gene.outputs[i] == bool(function.terms[i]):
                match_counts += 1
        self.score = match_counts * 100 / len(self.last_gene.outputs)

    def write_to_file(self, generation: int):
        f = open("answer.txt", "a")
        f.write('Generation ' f'{generation}:\n\n')
        text = ''
        for inp in range(INPUTS_COUNT ** 2):
            str_text = f'{inp:04b}', ': ', f'{int(self.last_gene.outputs[inp] == True)}\n'
            for s in str_text:
                text += s
        file_text = ' '.join(text)
        f.write(file_text)
        f.write(f'\nScore: {self.score}')
        f.write('\n----------------------------------\n\n\n')
        f.close()


def get_inputs(val):
    inputs = [f'{i:04b}' for i in range(TABLE_LENGTH ** 2)]
    res = []
    for string in inputs:
        res.append(string[3 - val])
    return res




