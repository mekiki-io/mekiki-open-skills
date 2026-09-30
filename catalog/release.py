from abc import ABC, abstractmethod


class Release(ABC):
    @abstractmethod
    def text(self) -> str: ...
