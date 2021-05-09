
import sys

sys.path.append('../src')
from DataFrame import DataFrame
from kNN import kNearestNeighbors

class kNN_classifier:

    """ The menu for net generating
        In the menu, user can pick the shape of structure - pressing 1.
        User also can define the numerical interval for generting values - pressing key 2.
        User has possibility to the quity program pressing key 3.
    """
    sample = []
    decision = []
    inputs = []

    def __init__(self):
        self.welcome_user()
        # initialize the NetGenerator object
        # assign here the net instance
        self.choices = {
            '1': self.get_sample,
            '2': self.classify,
            '3': self.quit_program
        }

    def welcome_user(self):
        """ Initial information on startup. """
        print(
            """
                Hello User! This program classifies the sample from input.
                1. Program reads the sample from user input.
                    1.A First value is considered as decision class.
                    2.B Other values are considered as inputs.
                """)

    def display_menu(self):
        """ The avaliable options to pick from the menu. """
        print("""
            1. Set the sample,
            2. Classify the sample,
            3. Quit the program.
            """)

    def run(self):
        """ The function runs the program and prints the output for specific option """
        while True:
            self.display_menu()
            choice = input("Choice: ").strip()
            self.temp = choice
            result = ''
            action = self.choices.get(choice)
            if action:
                action()
            else:
                print(f'The choice {choice} is invalid.')

    def quit_program(self):
        """ Function terminates the program """
        print('Program has been terminated.')
        sys.exit(0)

    def get_sample(self):

        self.dataframe = DataFrame()

        # get inputs and decision class
        self.inputs = self.dataframe.inputs
        self.decision = self.dataframe.decision_class

        try:
            for column, decision in zip(self.inputs[:5], self.decision[:5]):
                print(f'\n{column} => {decision}')
        except IndexError as e:
            print(e)

        answer = input(
            '\nPaste the sample with ";" delimitier among the values: ')

        if ';' not in answer:
            raise ValueError("The input does not contain delimiter.")

        values = answer.lstrip('-+').split(';')

        # validate if the values are numeric
        for value in values:
            testing = value.replace('.', '', 1)
            if not testing.isdigit():
                raise ValueError("The given value is not a digit.")

        filtered = list(filter(lambda x: x, values))

        # map the float convert
        values = list(map(lambda x: float(x), filtered))

        print(
            f'Your sample:\n\tinputs: {values[1:]}\n\tdecision_class: {values[0]}')

        self.sample = values

        return self

    def classify(self):

        if not self.sample:
            raise ValueError(f'The sample has not been created.')

        # set the classifier
        knn = kNearestNeighbors(k=3, metric='euclidean')

        try:
            if len(self.inputs[0]) != len(self.sample[1:]):
                raise ValueError(
                    "The length of sample is not equal as the data set.")
        except IndexError as e:
            print(e)

        # fit the knn
        knn.fit(self.inputs, self.decision)

        # predict the decision
        predicted = knn.predict([self.sample[1:]])

        if [self.sample[0]] == predicted[0]:
            print(
                f'Succesfully predicted: {[self.sample[0]]} = > {predicted[0]}')
        else:
            print(
                f'Unsuccessfull predict: {[self.sample[0]]} != {predicted[0]}')


if __name__ == '__main__':
    kNN_classifier().run()
