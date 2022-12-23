class miniStringFuck:

    def __init__(self, code):
        self.code = code
        self.cell = 0

    def start(self):
        out = ""
        for command in self.code:
            if command == "+":
                self.cell = (self.cell + 1) % 256
            elif command == ".":
                out += chr(self.cell)
        return out
    '''
    Набиваем + нужное число по ASCII таблице и с помошью . выводим его
    '''
