from typing import Callable
import math
import numpy as np

ActivationFunction = Callable[[float], float]


class Activations:

    @staticmethod
    def get(method_name: str) -> ActivationFunction:
        try:
            function: ActivationFunction = getattr(_Functions(), method_name)
        except AttributeError:
            raise NotImplementedError(
                "Activation function '{}' does not exist.".format(method_name))
        return function


class _Functions:

    @staticmethod
    def sigmoid(x: float) -> float:
        return 1 / (1 + math.exp(-x))

    @staticmethod
    def tanh(x: float) -> float:
        return np.tanh(x)
