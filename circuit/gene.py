from enum import Enum
INPUTS_COUNT = 4
class Gene:
    def __init__(self, input1, input2, gate, wire1, wire2, wire_out):
        self.input1 = input1
        self.input2 = input2
        self.gate = gate
        self.outputs = None
        self.wire1 = wire1
        self.wire2 = wire2
        self.wire_out = wire_out
        self.output()

    def output(self):
        if self.gate.value == 0:
            self.outputs = [self.input1[i] and self.input2[i] for i in range(INPUTS_COUNT ** 2)]
        elif self.gate.value == 1:
            self.outputs = [self.input1[i] or self.input2[i] for i in range(INPUTS_COUNT ** 2)]
        elif self.gate.value == 2:
            self.outputs = [not (self.input1[i] and self.input2[i]) for i in range(INPUTS_COUNT ** 2)]
        elif self.gate.value == 3:
            self.outputs = [not (self.input1[i] or self.input2[i]) for i in range(INPUTS_COUNT ** 2)]
        elif self.gate.value == 4:
            self.outputs = [self.input1[i] != self.input2[i] for i in range(INPUTS_COUNT ** 2)]
        elif self.gate.value == 5:
            self.outputs = [self.input1[i] == self.input2[i] for i in range(INPUTS_COUNT ** 2)]
        elif self.gate.value == 6:
            self.outputs = [self.input1[i] for i in range(INPUTS_COUNT ** 2)]
        elif self.gate.value == 7:
            self.outputs = [not self.input1[i] for i in range(INPUTS_COUNT ** 2)]




class Gate(Enum):
    AND = 0
    OR = 1
    NAND = 2
    NOR = 3
    XOR = 4
    XNOR = 5
    BUFFER = 6
    NOT = 7

