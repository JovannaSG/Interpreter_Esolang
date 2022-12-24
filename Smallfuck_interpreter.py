"""
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
"""


class Smallfuck:

    def __init__(self, code, tape):
        self.code_list = [x for x in code.replace("[]", "")]
        self.tape_list = [x for x in tape]
        self.code_pointer = 0
        self.tape_pointer = 0

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
            "*": self.__change_bit_value,  # меняем значение бита
            ">": self.__step_right,  # шаг вправо
            "<": self.__step_left,  # шаг влево
            "[": self.__open_bracket,  # проверка на вхождение в цикл и перемещение на ], если текущий бит 0
            "]": self.__closed_bracket  # проверка на выход из цикла и перемещение на [, если текущий бит 1
        }

        while self.code_pointer < len(self.code_list) \
                and self.tape_pointer >= 0 \
                and self.tape_pointer < len(self.tape_list):
            if self.code_list[self.code_pointer] in operations.keys():
                operations[self.code_list[self.code_pointer]]()

            self.code_pointer += 1

        return "".join(self.tape_list)

    def __change_bit_value(self):
        if self.tape_list[self.tape_pointer] == "0":
            self.tape_list[self.tape_pointer] = "1"
        else:
            self.tape_list[self.tape_pointer] = "0"

    def __step_right(self):
        self.tape_pointer += 1

    def __step_left(self):
        self.tape_pointer -= 1

    def __open_bracket(self):
        if self.tape_list[self.tape_pointer] == "0":
            self.code_pointer = self.closed_brackets[self.code_pointer]

    def __closed_bracket(self):
        if self.tape_list[self.tape_pointer] == "1":
            self.code_pointer = self.open_brackets[self.code_pointer]
