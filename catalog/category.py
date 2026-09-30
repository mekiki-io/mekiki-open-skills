from abc import ABC, abstractmethod
from typing import Any


class Category(ABC):
    @abstractmethod
    def id(self) -> str: ...

    @abstractmethod
    def document(self) -> Any: ...
