class boolFuck:

    def __init__(self, code, input=""):
        self.input = input
        self.code = code
        self.cptr = 0

        self.memory = {0: "0"}
        self.mptr = 0

        self.closed_brackets = {}
        self.open_brackets = {}
        brackets = []

        i = 0
        while i < len(self.code):
            if self.code[i] == "[":
                brackets.append(i)
            elif self.code[i] == "]":
                b = brackets.pop()
                self.closed_brackets[b] = i
                self.open_brackets[i] = b

            i += 1

        self.out_bits = [""]
        self.out_ptr = 0

        self.in_bits = []
        for char in input:
            self.in_bits.append(list(bin(ord(char))[2:].zfill(8)[::-1]))

    def start(self):
        commands = {
            "+": self.switch_bit,
            ",": self.read_input,
            ";": self.print_out,
            "<": self.move_mptr_left,
            ">": self.move_mptr_right,
            "[": self.open_bracket,
            "]": self.closed_bracket
        }

        while self.cptr < len(self.code):
            if self.code[self.cptr] in commands.keys():
                commands[self.code[self.cptr]]()

            self.cptr += 1

        result = ""

        if self.out_bits[self.out_ptr] == "":
            del self.out_bits[len(self.out_bits) - 1]
            self.out_ptr -= 1

        if self.input != "" and len(self.out_bits[self.out_ptr]) < 8:
            self.out_bits[self.out_ptr] = self.out_bits[self.out_ptr].zfill(8)

        for byte in self.out_bits:
            result += chr(int(byte, 2))

        return result

    def switch_bit(self):
        if self.memory[self.mptr] == "0":
            self.memory[self.mptr] = "1"
        else:
            self.memory[self.mptr] = "0"

    def move_mptr_left(self):
        self.mptr -= 1
        if self.mptr not in self.memory.keys():
            self.memory[self.mptr] = "0"

    def move_mptr_right(self):
        self.mptr += 1
        if self.mptr not in self.memory.keys():
            self.memory[self.mptr] = "0"

    def open_bracket(self):
        if self.memory[self.mptr] == "0":
            self.cptr = self.closed_brackets[self.cptr]

    def closed_bracket(self):
        if self.memory[self.mptr] == "1":
            self.cptr = self.open_brackets[self.cptr]

    def read_input(self):
        if len(self.in_bits) == 0:
            self.memory[self.mptr] = "0"
        else:
            self.memory[self.mptr] = self.in_bits[0].pop(0)

            if len(self.in_bits[0]) == 0:
                del self.in_bits[0]

    def print_out(self):
        self.out_bits[self.out_ptr] = str(self.memory[self.mptr]) + self.out_bits[self.out_ptr]

        if len(self.out_bits[self.out_ptr]) == 8:
            self.out_ptr += 1
            self.out_bits.append("")