class Painfuck:

    def __init__(self, code, iterations, width, height):
        self.code = code
        self.its = iterations
        self.width = width
        self.height = height
        self.code_ptr = 0
        self.grid = []

        self.x = 0
        self.y = 0

        i = 0
        row = [0] * width
        while i < height:
            self.grid.append(row.copy())
            i += 1

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

    def start(self):
        commands = {
            "n": self.__move_north,  # шаг вверх
            "s": self.__move_south,  # шаг вниз
            "e": self.__move_east,  # шаг вправо
            "w": self.__move_west,  # шаг влево
            "*": self.__change_bit_value,  # меняем значение бита
            "[": self.__open_bracket,  # проверка на вхождение в цикл и перемещение на ], если текущий бит 0
            "]": self.__closed_bracket  # проверка на выход из цикла и перемещение на [, если текущий бит 1
        }

        counter = 0
        while self.code_ptr < len(self.code) and counter < self.its:
            if self.code[self.code_ptr] in commands.keys():
                commands[self.code[self.code_ptr]]()
                counter += 1
            self.code_ptr += 1

        result = []
        for line in self.grid:
            str_line = ""
            for x in line:
                str_line += str(x)
            result.append(str_line)

        return "\r\n".join(result)

    def __change_bit_value(self):
        if self.grid[self.y][self.x] == 1:
            self.grid[self.y][self.x] = 0
        else:
            self.grid[self.y][self.x] = 1

    def __open_bracket(self):
        if self.grid[self.y][self.x] == 0:
            self.code_ptr = self.closed_brackets[self.code_ptr]

    def __closed_bracket(self):
        if self.grid[self.y][self.x] == 1:
            self.code_ptr = self.open_brackets[self.code_ptr]

    def __move_north(self):
        self.y = (self.y - 1) % self.height

    def __move_south(self):
        self.y = (self.y + 1) % self.height

    def __move_east(self):
        self.x = (self.x + 1) % self.width

    def __move_west(self):
        self.x = (self.x - 1) % self.width
