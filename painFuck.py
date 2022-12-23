class paintFuck:

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
            "n": self.move_north,  # шаг вверх
            "s": self.move_south,  # шаг вниз
            "e": self.move_east,  # шаг влево
            "w": self.move_west,  # шаг вправо
            "*": self.switch_bit,  # меняем значение бита
            "[": self.open_bracket,  # начало цикла
            "]": self.closed_bracket  # конец цикла
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

    def switch_bit(self):
        if self.grid[self.y][self.x] == 1:
            self.grid[self.y][self.x] = 0
        else:
            self.grid[self.y][self.x] = 1

    def open_bracket(self):
        if self.grid[self.y][self.x] == 0:
            self.code_ptr = self.closed_brackets[self.code_ptr]

    def closed_bracket(self):
        if self.grid[self.y][self.x] == 1:
            self.code_ptr = self.open_brackets[self.code_ptr]

    def move_north(self):
        self.y = (self.y - 1) % self.height

    def move_south(self):
        self.y = (self.y + 1) % self.height

    def move_east(self):
        self.x = (self.x + 1) % self.width

    def move_west(self):
        self.x = (self.x - 1) % self.width
