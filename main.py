from item import Item, ItemStack, Equipment, Consumable


class Inventory:
    max_slot = 10

    def __init__(self):
        self.__slot = Inventory.max_slot
        self.list_item = []

    def add_item(self, item: ItemStack):
        for i in self.list_item:
            if i.item is item.item:
                i.stack = item.stack
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

    @property
    def gold(self):
        return self.__gold

    @gold.setter
    def gold(self, value):
        self.__gold = max(0, self.__gold + value)

    @staticmethod
    def name_validation(name: str):
        return isinstance(name, str) and name.isalpha()


if __name__ == "__main__":
    print("UJI CLASS METHOD ")
    Item.base_price(15)
    print("Class method berhasil dipanggil")

    print("\nUJI OBJEK (INHERITANCE)")
    item1 = Equipment("Cangkul Besi", 2, durability=3)
    item2 = Consumable("Roti", 1, calorie=50)

    stack1 = ItemStack(item1, 1)
    stack2 = ItemStack(item2, 5)

    player1 = Character("Arthur")
    player2 = Character("Merlin")

    print("\nUJI METHOD OVERRIDING")
    print(item1.use())
    print(item2.use())
    print(f"Durability {item1._name} setelah dipakai: {item1.durability}")

    print("\nUJI INSTANCE METHOD ")
    print("Inventaris Sebelum:")
    player1.inventory.show_list_item()

    player1.inventory.add_item(stack1)
    player1.inventory.add_item(stack2)
    print("\nInventaris Sesudah:")
    player1.inventory.show_list_item()

    player1.inventory.add_item(ItemStack(item2, 3))
    print("\nInventaris Sesudah Ditambah Lagi (Roti +3, stack digabung):")
    player1.inventory.show_list_item()

    print("\nUJI ASOSIASI")
    player2.equip(item1)
    print(f"{player2.name} memegang: {player2.equipped._name}")
    print(player2.use_equipped())
    print(Character("Lancelot").use_equipped())

    print("\nUJI AGREGASI (Inventory dihapus, ItemStack tetap ada)")
    inv_agregasi = Inventory()
    stack_apel = ItemStack(Consumable("Apel", 1, calorie=30), 4)
    inv_agregasi.add_item(stack_apel)
    print("Inventory berisi:")
    inv_agregasi.show_list_item()

    del inv_agregasi  # hapus inventory
    print("\nInventory dihapus. ItemStack Apel masih ada:")
    print(stack_apel)

    print("\nUJI KOMPOSISI (Character dihapus, Inventory ikut hilang)")
    player3 = Character("Gawain")
    player3.inventory.add_item(ItemStack(Consumable("Madu", 1, calorie=20), 2))
    print(f"Inventory milik {player3.name}:")
    player3.inventory.show_list_item()

    del player3  # hapus Character
    try:
        print(player3.inventory)
    except NameError:
        print("\nCharacter dihapus, Inventory nya  juga akan ikut hilang ")

    print("\nUJI SETTER ")
    player1.gold = 100
    stack1.stack = 5
    print(f"Emas {player1.name} (Valid): {player1.gold}")
    print(f"Tumpukan Cangkul Besi (Valid): {stack1.stack}")

    player1.gold = -500
    stack1.stack = -10
    print(f"Emas {player1.name} (Tidak Valid -500): {player1.gold} (Tertahan di 0)")
    print(f"Tumpukan Cangkul Besi (Tidak Valid -10): {stack1.stack} (Tertahan di 0)")

    print("\nUJI HAPUS ITEM (INSTANCE METHOD) ")
    print("Inventaris Sebelum Dihapus:")
    player1.inventory.show_list_item()

    player1.inventory.delete_item_from_inventory()

    print("\nInventaris Sesudah Dihapus:")
    player1.inventory.show_list_item()

    print("\nUJI STATIC METHOD")
    uji_nama = Character.name_validation("Lancelot")
    print(f"Hasil static method untuk 'Lancelot': {uji_nama}")

    print("Uji coba membuat karakter dengan angka (akbar123)...")
    try:
        player_error = Character("akbar123")
    except ValueError as e:
        print(f"Error tertangkap: {e}")
