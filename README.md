# Program Simulasi Harvester

Program Python sederhana yang mensimulasikan sistem **item, inventaris, dan karakter** ala game RPG. Program ini dibuat untuk mendemonstrasikan konsep OOP (Object-Oriented Programming) di Python, meliputi **inheritance**, **relasi UML** (asosiasi, agregasi, komposisi), serta **enkapsulasi** (public, protected, private).

## Daftar Isi

- [Struktur File](#struktur-file)
- [Penjelasan Class](#penjelasan-class)
  - [1. Item (Superclass)](#1-item-superclass)
  - [2. Equipment (Subclass)](#2-equipment-subclass)
  - [3. Consumable (Subclass)](#3-consumable-subclass)
  - [4. ItemStack](#4-itemstack)
  - [5. Inventory](#5-inventory)
  - [6. Character](#6-character)
- [Penerapan Inheritance](#penerapan-inheritance)
- [Alur Program (`main`)](#alur-program-main)
- [Panduan Pengujian](#panduan-pengujian)

## Struktur File

```
.
├── item.py   # Item, Equipment, Consumable, ItemStack
├── main.py   # Inventory, Character, dan blok pengujian (if __name__ == "__main__")
└── README.md
```

`main.py` mengimpor class dari `item.py`:

```python
from item import Item, ItemStack, Equipment, Consumable
```

## Relasi UML

| Relasi        | Class                     | Penjelasan                                                                                                                                       |
| ------------- | ------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Asosiasi**  | `Character` → `Item`      | `Character` memegang referensi ke `Item` lewat atribut `equipped`. `Item` hidup mandiri dan tidak dimiliki oleh `Character`.                     |
| **Asosiasi**  | `ItemStack` → `Item`      | `ItemStack` menyimpan referensi ke `Item` yang ditumpuk.                                                                                         |
| **Agregasi**  | `Inventory` ◇ `ItemStack` | `ItemStack` dibuat di luar `Inventory`, lalu dimasukkan lewat `add_item()`. Jika `Inventory` dihapus, `ItemStack` masih bisa ada di tempat lain. |
| **Komposisi** | `Character` ◆ `Inventory` | `Inventory` dibuat di dalam `__init__` milik `Character`. Jika `Character` dihapus, `Inventory`-nya ikut hilang.                                 |

## Penjelasan Class

### 1. `Item` (Superclass)

Cetak biru untuk sebuah jenis barang di dalam game. Class ini menjadi **parent class** bagi `Equipment` dan `Consumable`.

| Anggota        | Tipe                             | Keterangan                                                                                     |
| -------------- | -------------------------------- | ---------------------------------------------------------------------------------------------- |
| `total_item`   | Atribut kelas (publik)           | Menghitung total objek `Item` (termasuk subclass) yang pernah dibuat.                          |
| `__base_price` | Atribut kelas (privat)           | Harga dasar pengali harga, nilai awal `10`. Diakses lewat _name mangling_ `_Item__base_price`. |
| `_name`        | Atribut instance (**protected**) | Nama item. Boleh diakses langsung oleh subclass.                                               |
| `__price`      | Atribut instance (**privat**)    | Harga akhir item. Hanya bisa diakses lewat property `price`.                                   |

**Konstruktor** `__init__(self, name, price)`

- Jika `price <= 0`, nilai dipaksa menjadi `10`.
- Harga akhir dihitung sebagai `price * Item.__base_price` **pada saat objek dibuat** (bukan properti dinamis, jadi perubahan `base_price` setelahnya tidak memengaruhi item yang sudah ada).
- Menambah `Item.total_item` sebanyak 1.

**Method `use(self)`**

- Perilaku bawaan: mengembalikan `"<name> digunakan"`. Method ini di-_override_ oleh subclass.

**Property `price`**

- _Getter_: mengembalikan `__price`.
- _Setter_: bersifat **inkremental**, yaitu `self.__price = max(0, self.__price + value)`. Artinya `item.price = 5` akan **menambah** 5 ke harga saat ini, dan tidak boleh kurang dari 0.

**Class Method `base_price(cls, value)`**

- Mengubah `__base_price` secara inkremental (`+= value`), dengan batas bawah 0.
- Berlaku global untuk item yang dibuat **setelah** pemanggilan ini.

**`__str__`**

- Format: `Nama: <name>\nHarga: <price>`.

### 2. `Equipment` (Subclass)

Item berupa peralatan yang bisa rusak, misalnya "Cangkul Besi". Mewarisi `Item`.

| Anggota      | Tipe                    | Keterangan                                            |
| ------------ | ----------------------- | ----------------------------------------------------- |
| `durability` | Atribut instance (unik) | Ketahanan peralatan. Berkurang 1 setiap kali dipakai. |

- **Konstruktor** `__init__(self, name, price, durability)`: memanggil `super().__init__(name, price)`, lalu menyimpan `durability`.
- **`use()` (override)**: jika `durability > 0`, durability dikurangi 1 dan mengembalikan `"Menggunakan Equipment <name>"`. Jika sudah `0`, mengembalikan pesan bahwa equipment rusak.
- **`__str__` (override)**: menambahkan baris `Ketahanan: <durability>`.

### 3. `Consumable` (Subclass)

Item yang bisa dikonsumsi, misalnya "Roti". Mewarisi `Item`.

| Anggota   | Tipe                    | Keterangan                                  |
| --------- | ----------------------- | ------------------------------------------- |
| `calorie` | Atribut instance (unik) | Jumlah kalori yang didapat saat dikonsumsi. |

- **Konstruktor** `__init__(self, name, price, calorie)`: memanggil `super().__init__(name, price)`, lalu menyimpan `calorie`.
- **`use()` (override)**: mengembalikan `"Mengkonsumsi <name>, dan mendapatkan <calorie> kalori"`.
- **`__str__` (override)**: menambahkan baris `Kalori: <calorie>`.

### 4. `ItemStack`

Membungkus satu `Item` (atau subclass-nya) beserta jumlah tumpukannya di dalam inventaris, mirip slot item pada game yang bisa menampung banyak barang sejenis.

| Anggota   | Tipe                      | Keterangan                                 |
| --------- | ------------------------- | ------------------------------------------ |
| `item`    | Atribut instance          | Objek `Item` yang ditumpuk (**asosiasi**). |
| `__stack` | Atribut instance (privat) | Jumlah item dalam tumpukan tersebut.       |

**Property `stack`**

- _Getter_: mengembalikan `__stack`.
- _Setter_: inkremental seperti pada `Item.price`, yaitu `self.__stack = max(0, self.__stack + value)`.

**`__str__`**

- Menggabungkan representasi `Item` dengan baris tambahan `Tumpukan: <stack>`.

### 5. `Inventory`

Mengelola kumpulan `ItemStack` milik seorang karakter, dengan kapasitas slot terbatas.

| Anggota     | Tipe                      | Keterangan                                      |
| ----------- | ------------------------- | ----------------------------------------------- |
| `max_slot`  | Atribut kelas             | Kapasitas maksimum slot (default `10`).         |
| `__slot`    | Atribut instance (privat) | Disalin dari `max_slot` saat inventaris dibuat. |
| `list_item` | Atribut instance          | List berisi objek `ItemStack` (**agregasi**).   |

**`add_item(self, item: ItemStack)`**

- Mencari `ItemStack` yang berisi **item yang sama** (`i.item is item.item`). Jika ada, jumlah stack ditambahkan lewat setter `stack` (yang sudah bersifat inkremental).
- Jika belum ada dan slot masih tersedia, `ItemStack` baru ditambahkan ke list.
- Jika slot penuh, mencetak `"Maaf, Inventaris Penuh"`.

**`delete_item_from_inventory(self)`**

- Menghapus `ItemStack` yang jumlah stack-nya `0`.

**`show_list_item(self)`**

- Mencetak seluruh isi inventaris menggunakan `__str__` masing-masing `ItemStack`.

### 6. `Character`

Cetak biru karakter pemain, memiliki nama, emas (_gold_), inventaris sendiri, dan item yang sedang dipegang.

| Anggota     | Tipe                      | Keterangan                                                  |
| ----------- | ------------------------- | ----------------------------------------------------------- |
| `name`      | Atribut instance          | Nama karakter (divalidasi saat pembuatan).                  |
| `__gold`    | Atribut instance (privat) | Jumlah emas, awal `0`.                                      |
| `inventory` | Atribut instance          | Objek `Inventory` baru untuk tiap karakter (**komposisi**). |
| `equipped`  | Atribut instance          | Item yang sedang dipegang, awalnya `None` (**asosiasi**).   |

**Konstruktor `__init__(self, name)`**

- Memanggil `name_validation(name)`; jika `False`, melempar `ValueError("Nama tidak boleh mengandung angka")`.

**`equip(self, item)`**

- Mengisi `equipped` dengan item yang diberikan.

**`use_equipped(self)`**

- Jika `equipped` kosong, mengembalikan `"Tidak ada item yang dipegang"`. Jika ada, memanggil `use()` milik item tersebut. Karena method ini memanggil `use()` pada tipe item yang berbeda (`Equipment` atau `Consumable`), hasilnya menyesuaikan dengan tipe aslinya (polimorfisme).

**Property `gold`**

- _Getter_: mengembalikan `__gold`.
- _Setter_: inkremental dan tidak boleh negatif, yaitu `self.__gold = max(0, self.__gold + value)`.

**Static Method `name_validation(name)`**

- Mengembalikan `True` jika `name` adalah `str` dan seluruhnya huruf (`str.isalpha()`, tidak boleh ada angka, spasi, atau simbol).
- Dipanggil tanpa instance: `Character.name_validation(...)`.

## Penerapan Inheritance

| Syarat                  | Penerapan                                                                                                       |
| ----------------------- | --------------------------------------------------------------------------------------------------------------- |
| Superclass dan subclass | Superclass `Item`; subclass `Equipment` dan `Consumable`.                                                       |
| Penggunaan `super()`    | `super().__init__(name, price)` di konstruktor kedua subclass. `super().__str__()` di `__str__` kedua subclass. |
| Atribut unik subclass   | `Equipment.durability` dan `Consumable.calorie`.                                                                |
| Method overriding       | `use()` dan `__str__()` di-override di kedua subclass dengan perilaku berbeda.                                  |
| Protected               | `_name` di `Item`, dipakai langsung oleh `use()` milik subclass.                                                |
| Private                 | `__price` dan `__base_price` di `Item`, hanya diakses lewat property dan class method.                          |

## Alur Program (`main`)

Blok `if __name__ == "__main__":` menjalankan skenario pengujian berurutan:

1. **Uji Class Method**: memanggil `Item.base_price(15)`, sehingga `__base_price` naik dari `10` menjadi `25`.
2. **Uji Objek (Inheritance)**: membuat `Equipment` "Cangkul Besi" (harga input `2`, durability `3`) dan `Consumable` "Roti" (harga input `1`, kalori `50`), dua `ItemStack`, lalu dua `Character` (`Arthur`, `Merlin`).
3. **Uji Method Overriding**: memanggil `use()` pada kedua item untuk menunjukkan perilaku yang berbeda, dan menampilkan durability yang berkurang.
4. **Uji Instance Method**: menambahkan `stack1` dan `stack2` ke inventaris Arthur, lalu menambahkan `ItemStack` baru berisi Roti (3 buah) untuk menguji penggabungan stack, sehingga jumlah Roti menjadi 8.
5. **Uji Asosiasi**: `Merlin` memegang Cangkul Besi lewat `equip()`, lalu memakainya lewat `use_equipped()`. Karakter yang belum memegang apa pun menampilkan pesan bawaan.
6. **Uji Agregasi**: `ItemStack` Apel dibuat di luar, lalu dimasukkan ke sebuah `Inventory` terpisah. Setelah `Inventory` dihapus dengan `del`, `ItemStack` Apel masih bisa dicetak.
7. **Uji Komposisi**: `Character` "Gawain" dibuat beserta `Inventory`-nya. Setelah `Character` dihapus dengan `del`, `Inventory` miliknya tidak bisa diakses lagi (menghasilkan `NameError`).
8. **Uji Setter**: menguji setter `gold` dan `stack` dengan nilai positif lalu nilai negatif besar, memastikan hasil tertahan di `0`.
9. **Uji Hapus Item**: karena `stack1` sudah `0`, `delete_item_from_inventory()` menghapusnya dari daftar.
10. **Uji Static Method**: memanggil `Character.name_validation("Lancelot")` dan mencoba membuat `Character("akbar123")` untuk menguji penanganan `ValueError`.

## Panduan Pengujian

### Cara Menjalankan

```bash
python3 main.py
```

Membutuhkan **Python 3.12 atau lebih baru** (karena `from typing import override`), tanpa modul eksternal. Pada Python yang lebih lama, ganti impor tersebut dengan `from typing_extensions import override` atau hapus dekorator `@override`.

### Uji Manual

Beberapa hal yang dapat dicoba untuk pengujian lebih lanjut:

- **Inventaris penuh**: tambahkan lebih dari `Inventory.max_slot` (10) jenis item berbeda ke satu inventaris, lalu pastikan pesan `"Maaf, Inventaris Penuh"` muncul saat slot ke-11 ditambahkan.
- **Perubahan `base_price` di tengah permainan**: buat satu `Item` sebelum dan satu lagi sesudah memanggil `Item.base_price(...)`, lalu bandingkan harganya untuk memastikan harga hanya dihitung sekali saat objek dibuat.
- **Equipment rusak**: panggil `use()` pada `Equipment` lebih dari jumlah `durability`-nya, lalu pastikan pesan "rusak" muncul.
- **Item berbeda objek**: buat dua `Consumable` dengan nama sama tetapi objek berbeda, lalu tambahkan ke inventaris. Keduanya dianggap item berbeda karena perbandingan memakai identitas objek (`is`).
