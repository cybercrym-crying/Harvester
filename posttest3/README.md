# Posttest 3 – Game Inventaris & Peternakan (OOP Python)

Program simulasi sederhana bergaya game RPG. Seorang `Character` memiliki `Inventory`, dapat memegang `Item` (Equipment/Consumable), dan memanen hasil dari hewan ternak (`Cow`, `Chicken`) yang menghasilkan `ItemStack` yang disimpan ke inventaris. Program ini menerapkan **Abstraksi (ABC)**, **Polimorfisme**, dan **relasi antar kelas** (asosiasi, agregasi, komposisi).

Struktur file:

| File | Isi |
|------|-----|
| `item.py` | `Item` (abstract), `Equipment`, `Consumable`, `ItemStack` |
| `animal.py` | `Animal` (abstract), `Cow`, `Chicken` |
| `main.py` | `Inventory`, `Character`, `Merchant`, `Blacksmith`, dan program uji |

Cara menjalankan (butuh Python 3.12+ karena memakai `typing.override`):

```
python main.py
```

---

## 1. Class Diagram

<img width="856" height="541" alt="image" src="https://github.com/user-attachments/assets/c7572f1c-00d7-4c9f-a5b2-fd76949f62c5" />


### Penjelasan Relasi

- **Asosiasi** – `Character` → `Item` (atribut `equipped`, diisi lewat `equip()`), dan `ItemStack` → `Item` (atribut `item`). Objek `Item` dibuat di luar dan hanya dirujuk, tidak ada kepemilikan; satu `Item` bisa dipegang atau dirujuk banyak objek.
- **Agregasi** – `Inventory` ◇— `ItemStack` (atribut `list_item`). `ItemStack` dibuat di luar `Inventory` lalu dimasukkan lewat `add_item()`, sehingga bila `Inventory` dihapus `ItemStack` tetap ada. Ini dibuktikan di bagian "UJI AGREGASI" pada `main.py` (`stack_batu` masih bisa dicetak setelah `del inv_agregasi`). Karena itu relasinya agregasi, bukan komposisi.
- **Komposisi** – `Character` ◆— `Inventory`. `Inventory` dibuat langsung di dalam `Character.__init__()` (`self.inventory = Inventory()`), sehingga umurnya terikat pada `Character`: bila `Character` dihapus, `Inventory`-nya ikut hilang. Ini dibuktikan di bagian "UJI KOMPOSISI".

Relasi tambahan pada diagram: pewarisan (`Equipment`, `Consumable` → `Item`; `Cow`, `Chicken` → `Animal`) dan dependensi putus-putus (`Character.harvest()` memakai `Animal`; `Animal.produce()` membuat `ItemStack`).

---

## 2. Abstraksi

- **Abstract class:** `Item` (`item.py`) dengan abstract method `use()` dan `get_category()`; `Animal` (`animal.py`) dengan abstract method `speak()` dan `produce()`. Keduanya mewarisi `ABC`.
- **Subclass yang mengimplementasikan seluruh abstract method:** `Equipment` dan `Consumable` (untuk `Item`); `Cow` dan `Chicken` (untuk `Animal`).
- **Method konkret yang dipakai bersama:** `Animal.feed()` (dipakai `Cow` dan `Chicken` tanpa override) dan `Item.__str__()` serta properti `price` (dipakai semua turunan `Item`).
- **Bukti tidak bisa diinstansiasi:** bagian "UJI ABSTRAKSI" di `main.py` memakai `try-except TypeError`; hasilnya ada pada screenshot di bawah.
- **Inheritance:** subclass memakai `super().__init__(...)`, punya atribut unik (`durability`, `calorie`), serta atribut protected (`_name`) dan private (`__price`, `__stack`, `__gold`).

## 3. Polimorfisme

- **Via pewarisan:** `use()` dan `get_category()` di-override oleh `Equipment` dan `Consumable` dengan perilaku berbeda; `speak()` dan `produce()` di-override oleh `Cow` dan `Chicken`. Semuanya dipanggil lewat satu loop pada list berisi objek subclass berbeda (`list_items` dan `hewan_ternak`).
- **Duck typing:** `Merchant` dan `Blacksmith` tidak berhubungan lewat pewarisan, tetapi sama-sama punya method `interact()` dan dipanggil lewat satu fungsi `npc_interaction(npc)`.
- **Operator overloading:** `ItemStack.__add__()` menggabungkan dua tumpukan item yang sama (`stack1 + stack2`); `__str__()` dipakai di beberapa kelas.
- **Tanpa anti-pattern:** tidak ada rantai `if/elif` yang mengecek `type()` atau string jenis; tiap objek menentukan perilakunya sendiri lewat method.


