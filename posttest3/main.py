from abc import ABC, abstractmethod
from typing import override
from item import Item, ItemStack, Equipment, Consumable
from animal import *


class Inventory:
    max_slot = 10

    def __init__(self):
        self.__slot = Inventory.max_slot
        self.list_item = []

    def add_item(self, item: ItemStack):
        for i in self.list_item:
            if i.item is item.item:
                i.stack += item.stack
                return
        if len(self.list_item) < self.__slot:
            self.list_item.append(item)
        else:
            print("Maaf, Inventaris Penuh")

    def delete_item_from_inventory(self):
        self.list_item = [i for i in self.list_item if i.stack > 0]

    def show_list_item(self):
        for i in self.list_item:
            print(i)
            print("-" * 15)


class Character:
    def __init__(self, name):
        if not self.name_validation(name):
            raise ValueError("Nama tidak boleh mengandung angka")
        self.name = name
        self.__gold = 0
        self.inventory = Inventory()
        self.equipped = None

    def equip(self, item: Item):
        self.equipped = item

    def use_equipped(self):
        if self.equipped is None:
            return "Tidak ada item yang dipegang"
        return self.equipped.use()

    def harvest(self, animal: Animal):
        hasil_panen = animal.produce()
        print(f"{self.name} memanen {hasil_panen.item._name} dari {animal.name}")
        self.inventory.add_item(hasil_panen)

    @property
    def gold(self):
        return self.__gold

    @gold.setter
    def gold(self, value):
        self.__gold = max(0, self.__gold + value)

    @staticmethod
    def name_validation(name: str):
        return isinstance(name, str) and name.isalpha()


class Merchant:
    def interact(self):
        return "Merchant: Selamat datang pertualang apa ada yang ingin di beli?"


class Blacksmith:
    def interact(self):
        return "Blacksmith: Mau beli perlengkapan apa petualang?"


def npc_interaction(npc):
    print(npc.interact())


if __name__ == "__main__":
    print("UJI ABSTRAKSI ")
    try:
        item_base = Item("Batu", 1)
    except TypeError as e:
        print("BERHASIL: Tidak bisa membuat objek dari abstract class Item")
        print(f"Error: {e}")

    try:
        hewan_base = Animal("Misterius")
    except TypeError as e:
        print("BERHASIL: Tidak bisa membuat objek dari abstract class Animal")
        print(f"Error: {e}\n")

    print("UJI POLIMORISME DARI PEWARISAN ")
    item1 = Equipment("Pedang Besi", 5, durability=10)
    item2 = Consumable("Ramuan Darah", 2, calorie=100)

    print("Polimorisme Item")
    list_items = [item1, item2]
    for obj in list_items:
        print(f"Kategori: {obj.get_category()} \t| Aksi: {obj.use()}")

    print("\nPolimorisme Animal")
    sapi = Cow("Bessie")
    ayam = Chicken("Henrietta")
    hewan_ternak = [sapi, ayam]
    for hewan in hewan_ternak:
        print(hewan.feed())
        print(hewan.speak())
    print()

    print("UJI DUCK TYPING ")
    penjual = Merchant()
    pandai_besi = Blacksmith()
    npc_interaction(penjual)
    npc_interaction(pandai_besi)
    print()

    print("UJI OVERLOADING ")
    stack_apel1 = ItemStack(Consumable("Apel", 1, calorie=30), 2)
    stack_apel2 = ItemStack(Consumable("Apel", 1, calorie=30), 3)
    stack_gabungan = stack_apel1 + stack_apel2
    print("Hasil penggabungan stack apel via magic method (__add__):")
    print(stack_gabungan)
    print()

    print("UJI ASOSIASI & INTERAKSI ")
    player1 = Character("Arthur")
    player1.equip(item1)
    print(f"{player1.name} memegang: {player1.equipped._name}")
    print(player1.use_equipped())

    print(f"\n{player1.name} mulai bertani:")
    player1.harvest(sapi)
    player1.harvest(ayam)
    print(f"\nIsi Inventory {player1.name} setelah panen:")
    player1.inventory.show_list_item()
    print()

    print("UJI AGREGASI ")
    inv_agregasi = Inventory()
    stack_batu = ItemStack(Consumable("Batu", 1, calorie=0), 5)
    inv_agregasi.add_item(stack_batu)

    del inv_agregasi
    print("Inventory dihapus tapi objek ItemStack Batu masih eksis:")
    print(stack_batu)
    print()

    print("UJI KOMPOSISI ")
    player3 = Character("Gawain")
    player3.inventory.add_item(ItemStack(Consumable("Madu", 1, calorie=20), 2))

    del player3
    try:
        print(player3.inventory)
    except NameError:
        print(
            "BERHASIL: Saat Character dihapus, instance Inventory miliknya ikut musnah karena dibuat langsung di dalam class player\n"
        )
