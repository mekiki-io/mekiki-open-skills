from abc import ABC, abstractmethod

from catalog.category import Category


class Catalog(ABC):
    @abstractmethod
    def categories(self) -> list[Category]: ...
