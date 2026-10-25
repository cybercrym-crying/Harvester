from abc import ABC, abstractmethod
from typing import override
from item import *


class Animal(ABC):
    def __init__(self, name: str):
        self.name = name

    def feed(self):
        return f"{self.name} sedang makan."

    @abstractmethod
    def speak(self) -> str:
        pass

    @abstractmethod
    def produce(self) -> ItemStack:
        pass


class Cow(Animal):
    def __init__(self, name: str):
        super().__init__(name)

    @override
    def speak(self) -> str:
        return f"{self.name} berkata: Moooo!"

    @override
    def produce(self) -> ItemStack:
        susu = Consumable("Susu Segar", price=5, calorie=150)
        return ItemStack(susu, 1)


class Chicken(Animal):
    def __init__(self, name: str):
        super().__init__(name)

    @override
    def speak(self) -> str:
        return f"{self.name} berkata: Petok petok!"

    @override
    def produce(self) -> ItemStack:
        telur = Consumable("Telur Ayam", price=2, calorie=70)
        return ItemStack(telur, 1)
