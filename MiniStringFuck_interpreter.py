"""
MiniStringFuck является производным от известного Brainfuck,
который содержит ячейку памяти в качестве единственной формы хранения данных, в отличие от ленты памяти из 30 000 ячеек в Brainfuck.
Ячейка памяти в MiniStringFuck изначально начинается с 0. MiniStringFuck содержит только 2 команды, а не 8:

+ - Увеличение ячейки памяти. Если он достигает 256, выполнить перенос на 0.
. - Вывести значение ячейки памяти как символ с кодовой точкой, равной значению
"""


class MiniStringFuck:

    def __init__(self, code):
        self.code = code
        self.cell = 0

    '''
        Набиваем плюсами нужное число по ASCII таблице и с помощью . выводим его
    '''
    def start(self):
        result = ""
        for i in self.code:
            if i == "+":
                self.cell = (self.cell + 1) % 256
            elif i == ".":
                result += chr(self.cell)
        return result
