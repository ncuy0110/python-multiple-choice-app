from random import randint


class Questions:
    def __init__(self, data):
        self.questions = data['questions']
        self.answers = data['answers']

    def get_amount(self):
        return len(self.questions)

    def get_question(self, index):
        return self.questions[index]

    def check_answer(self, question, option):
        if self.answers[question] == option:
            return True
        return False

    def change_position(self):
        for i in range(20):
            a = randint(0, self.get_amount()-1)
            b = randint(0, self.get_amount() - 1)
            self.questions[a], self.questions[b] = self.questions[b], self.questions[a]
            self.answers[a], self.answers[b] = self.answers[b], self.answers[a]
