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
        self.outputs = []
        for i in range (2 ** INPUTS_COUNT):
            if self.gate.value == 0: #AND
                if self.input1[i] == self.input2[i] == 1:
                    self.outputs.append(1)
                else: self.outputs.append(0)
            elif self.gate.value == 1: #OR
                if self.input1[i] == 1 or self.input2[i] == 1:
                    self.outputs.append(1)
                else: self.outputs.append(0)
            elif self.gate.value == 2: #NAND
                if self.input1[i] == self.input2[i] == 1:
                    self.outputs.append(0)
                else: self.outputs.append(1)
            elif self.gate.value == 3:
                if self.input1[i] == self.input2[i] == 0:
                    self.outputs.append(1)
                else: self.outputs.append(0)
            elif self.gate.value == 4:
                if self.input1[i] == self.input2[i]:
                    self.outputs.append(0)
                else: self.outputs.append(1)
            elif self.gate.value == 5:
                if self.input1[i] == self.input2[i]:
                    self.outputs.append(1)
                else: self.outputs.append(0)
            elif self.gate.value == 6:
                self.outputs.append(self.input1[i])
            elif self.gate.value == 7:
                self.outputs.append(1 - int(self.input1[i]))





class Gate(Enum):
    AND = 0
    OR = 1
    NAND = 2
    NOR = 3
    XOR = 4
    XNOR = 5
    BUFFER = 6
    NOT = 7

