from abc import ABC, abstractmethod


class Check(ABC):
    @abstractmethod
    def problems(self) -> list[str]: ...
