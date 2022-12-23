class smallFuck:

    def __init__(self, code, tape):
        self.code_list = [x for x in code.replace("[]", "")]
        self.tape_list = [x for x in tape]
        self.code_ptr = 0
        self.tape_ptr = 0

        self.closed_brackets = {}
        self.open_brackets = {}
        brackets = []

        i = 0
        while i < len(self.code_list):
            if self.code_list[i] == "[":
                brackets.append(i)
            elif self.code_list[i] == "]":
                b = brackets.pop()
                self.closed_brackets[b] = i
                self.open_brackets[i] = b
            i += 1

    def start(self):
        operations = {
            "*": self.switch_bit,  # меняем значение бита
            ">": self.step_forward,  # шаг вправо
            "<": self.step_backwards,  # шаг влево
            "[": self.open_bracket,  # начало цикла
            "]": self.closed_bracket  # конец цикла
        }

        while self.code_ptr < len(self.code_list) and self.tape_ptr >= 0 and self.tape_ptr < len(self.tape_list):
            if self.code_list[self.code_ptr] in operations.keys():
                operations[self.code_list[self.code_ptr]]()

            self.code_ptr += 1

        return "".join(self.tape_list)

    def switch_bit(self):
        if self.tape_list[self.tape_ptr] == "0":
            self.tape_list[self.tape_ptr] = "1"
        else:
            self.tape_list[self.tape_ptr] = "0"

    def step_forward(self):
        self.tape_ptr += 1

    def step_backwards(self):
        self.tape_ptr -= 1

    def open_bracket(self):
        if self.tape_list[self.tape_ptr] == "0":
            self.code_ptr = self.closed_brackets[self.code_ptr]

    def closed_bracket(self):
        if self.tape_list[self.tape_ptr] == "1":
            self.code_ptr = self.open_brackets[self.code_ptr]


'''
    Smallfuck — еще более лаконичный диалект языка Brainfuck, который оперирует не байтами, а битами, 
    имеет ограниченную емкость памяти и не определяет команды ввода-вывода. Таким образом, остается всего 5 команд:

    * : инвертировать бит в текущей ячейке;
    > : сдвинуть указатель данных на один бит вправо;
    < : сдвинуть указатель данных на один бит влево;
    [ : “начало цикла”: если текущий бит = 1, сдвинуть указатель инструкций на одну команду вправо, 
    иначе сдвинуть его на команду, следующую за парной командой ];
    ] : “конец цикла”: если текущий бит = 0, сдвинуть указатель инструкций на одну команду вправо, 
    иначе сдвинуть его на команду, следующую за парной командой [. 
    Может также быть представлен как безусловный переход указателя инструкций на парную команду [, 
    т.к. [ выполняет отдельную проверку на вход в тело цикла;
    Поскольку команды ввода-вывода не определены, считается, что входные данные закодированы как начальные состояния памяти, 
    а выходные — считываются из памяти после конца работы программы. 
    Таким образом, язык может рассматриваться как автомат по преобразованию состояний памяти; 
    для оценки работы программы ее следует запускать на всех возможных входных состояниях памяти, 
    или же оговаривать нужное состояние.

    Из-за ограниченности размеров памяти язык не является Тьюринг-полным и принадлежит к классу машин с ограниченной памятью.
'''
