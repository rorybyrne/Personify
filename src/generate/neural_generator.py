from generate.base_generator import BaseGenerator
from keras.models import Sequential
from keras.layers import Dense

class NeuralGenerator(BaseGenerator):
    def __init__(self):
        BaseGenerator.__init__(self)
        self.model = self.construct_model()

    def generate(self, char_count):
        pass

    def construct_model(self):
        '''
            Construct the model
        :return `model`:
        '''
        # TODO

        model = Sequential()
        model.add(Dense(10))

        return model

