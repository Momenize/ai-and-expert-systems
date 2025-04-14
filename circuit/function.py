import random

num_of_inputs = 4
class Function:
    def __init__(self):
        self.terms = []
        # self.terms.extend([0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0])
        for i in range(2 ** num_of_inputs):
            self.terms.append(random.randint(0, 1))
        self.write_to_file()

    def write_to_file(self):
        f = open("given_table.txt", "w")
        for i in range(num_of_inputs ** 2):
            text = f'{i:04b}', ': ', f'{self.terms[i]}'
            string_text = ' '.join(text)
            f.write(string_text)
            f.write('\n')

