class Boolfuck:

    def __init__(self, code, user_input=""):
        self.user_input = user_input
        self.code = code
        self.code_pointer = 0

        self.memory = {0: "0"}
        self.memory_pointer = 0

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
        for char in user_input:
            self.in_bits.append(list(bin(ord(char))[2:].zfill(8)[::-1]))  # Заполняем нулями до 8

    def start(self):
        commands = {
            "+": self.__change_bit_value,  # меняем значение бита
            ",": self.__read_user_input,  # считываем, что ввёл пользователь
            ";": self.__print_to_output_stream,  # вывод на поток
            "<": self.__move_memory_pointer_left,  # перемещение указателя памяти влево
            ">": self.__move_memory_pointer_right,  # перемещение указателя памяти влево
            "[": self.__open_bracket,  # проверка на вхождение в цикл и перемещение на ], если текущий бит 0
            "]": self.__closed_bracket  # проверка на выход из цикла и перемещение на [, если текущий бит 1
        }

        while self.code_pointer < len(self.code):
            if self.code[self.code_pointer] in commands.keys():
                commands[self.code[self.code_pointer]]()

            self.code_pointer += 1

        result = ""

        if self.out_bits[self.out_ptr] == "":
            del self.out_bits[len(self.out_bits) - 1]
            self.out_ptr -= 1

        if self.user_input != "" and len(self.out_bits[self.out_ptr]) < 8:
            self.out_bits[self.out_ptr] = self.out_bits[self.out_ptr].zfill(8)

        for byte in self.out_bits:
            result += chr(int(byte, 2))

        return result

    def __change_bit_value(self):
        if self.memory[self.memory_pointer] == "0":
            self.memory[self.memory_pointer] = "1"
        else:
            self.memory[self.memory_pointer] = "0"

    def __move_memory_pointer_left(self):
        self.memory_pointer -= 1
        if self.memory_pointer not in self.memory.keys():
            self.memory[self.memory_pointer] = "0"

    def __move_memory_pointer_right(self):
        self.memory_pointer += 1
        if self.memory_pointer not in self.memory.keys():
            self.memory[self.memory_pointer] = "0"

    def __open_bracket(self):
        if self.memory[self.memory_pointer] == "0":
            self.code_pointer = self.closed_brackets[self.code_pointer]

    def __closed_bracket(self):
        if self.memory[self.memory_pointer] == "1":
            self.code_pointer = self.open_brackets[self.code_pointer]

    def __read_user_input(self):
        if len(self.in_bits) == 0:
            self.memory[self.memory_pointer] = "0"
        else:
            self.memory[self.memory_pointer] = self.in_bits[0].pop(0)

            if len(self.in_bits[0]) == 0:
                del self.in_bits[0]

    def __print_to_output_stream(self):
        self.out_bits[self.out_ptr] = str(self.memory[self.memory_pointer]) + self.out_bits[self.out_ptr]

        if len(self.out_bits[self.out_ptr]) == 8:
            self.out_ptr += 1
            self.out_bits.append("")
