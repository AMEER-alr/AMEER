from abc import ABC, abstractmethod
from .pet import Pet

class Animal(Pet, ABC):
    def __init__(self, name: str, age: int):
        self._name = name
        self._age = age

    def happy_birthday(self):
        self._age += 1

    def get_name(self):
        return self._name

    def get_age(self):
        return self._age

    @abstractmethod
    def express(self):
        pass

    @abstractmethod
    def get_age_in_human_years(self):
        pass