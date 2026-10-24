from typing import override
from abc import ABC, abstractmethod


class Item(ABC):
    total_item = 0
    __base_price = 10

    def __init__(self, name: str, price: int):
        if price <= 0:
            price = 10
        self._name = name
        self.__price = price * Item.__base_price
        Item.total_item += 1

    def __str__(self):
        return f"Nama: {self._name}\nHarga: {self.__price}"

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, value: int):
        self.__price = max(0, self.__price + value)

    @classmethod
    def base_price(cls, value):
        cls.__base_price = max(0, cls.__base_price + value)

    @abstractmethod
    def use(self) -> str:
        pass

    @abstractmethod
    def get_category(self) -> str:
        pass


class Equipment(Item):
    def __init__(self, name, price, durability):
        super().__init__(name, price)
        self.durability = durability

    def __str__(self):
        return f"{super().__str__()}\nKetahanan: {self.durability}"

    @override
    def use(self):
        if self.durability > 0:
            self.durability -= 1
            return f"Menggunakan Equipment {self._name}"
        return f"Equipment {self._name} rusak, tidak dapat digunakan"

    @override
    def get_category(self) -> str:
        return "Equipment"


class Consumable(Item):
    def __init__(self, name, price, calorie):
        super().__init__(name, price)
        self.calorie = calorie

    def __str__(self):
        return f"{super().__str__()}\nKalori: {self.calorie}"

    @override
    def use(self):
        return f"Mengkonsumsi {self._name}, dan mendapatkan {self.calorie} kalori"

    @override
    def get_category(self) -> str:
        return "Consumable"


class ItemStack:
    def __init__(self, item: Item, stack: int):
        self.item = item
        self.__stack = stack

    def __str__(self):
        return f"{self.item.__str__()}\nTumpukan: {self.__stack}"

    def __add__(self, other):
        if isinstance(other, ItemStack) and self.item._name == other.item._name:
            return ItemStack(self.item, self.stack + other.stack)
        raise ValueError(
            "Hanya bisa menggabungkan ItemStack dengan nama item yang sama!"
        )

    @property
    def stack(self):
        return self.__stack

    @stack.setter
    def stack(self, value: int):
        self.__stack = max(0, self.__stack + value)
