from abc import ABC, abstractmethod


class Agent(ABC):
    def __init__(self, input_shape, output_shape):
        self.input_shape = input_shape
        self.output_shape = output_shape


