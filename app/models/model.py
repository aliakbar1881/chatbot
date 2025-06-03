from abc import ABC, abstractmethod


class Model(ABC):
    def __init__(self, model_name: str):
        self.model_name = model_name

    @abstractmethod
    def generate(self, query):
        pass

    @abstractmethod
    def __call__(self, *args: Any, **kwds: Any) -> None:
        pass

    @abstractmethod
    def get(self):
        pass
