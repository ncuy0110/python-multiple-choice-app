class Student:
    def __init__(self):
        self.ID = None
        self.name = None
        self.numbers = None
        self.selection = [-1]*10
        self.selecting = 0

    def choose_option(self, option):
        self.selection[self.selecting] = option

    def set_name(self, name):
        self.name = name

    def set_ID(self, ID):
        self.ID = ID

    def set_numbers(self, numbers):
        self.numbers = numbers
