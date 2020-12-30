from typing import Callable
import math
import numpy as np

ActivationFunction = Callable[[float], float]


class Activations:

    @staticmethod
    def get(method_name: str) -> ActivationFunction:
        try:
            function: ActivationFunction = getattr(Functions(), method_name)
        except AttributeError:
            raise NotImplementedError("Class `{}` does not implement `{}`".format(
                Functions().__class__.__name__, method_name))
        return function


class Functions:

    @staticmethod
    def sigmoid(x: float) -> float:
        return 1 / (1 + math.exp(-x))

    @staticmethod
    def tanh(x: float) -> float:
        return np.tanh(x)
