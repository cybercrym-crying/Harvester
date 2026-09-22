# Program Simulasi Harvester

Program Python sederhana yang mensimulasikan sistem **item, inventaris, dan karakter** ala game RPG. Program ini dibuat untuk mendemonstrasikan konsep OOP (Object-Oriented Programming) di Python

## Daftar Isi

- [Struktur File](#struktur-file)
- [Penjelasan Class](#penjelasan-class)
  - [1. Item](#1-item)
  - [2. ItemStack](#2-itemstack)
  - [3. Inventory](#3-inventory)
  - [4. Character](#4-character)
- [Alur Program (`main`)](#alur-program-main)
- [Panduan Pengujian](#panduan-pengujian)
- [Catatan Teknis](#catatan-teknis)

## Struktur File

```
.
└── main.py   # Berisi semua class dan blok pengujian (if __name__ == "__main__")
```

## Penjelasan Class

### 1. `Item`

Cetak biru untuk sebuah jenis barang di dalam game (misalnya "Cangkul Besi").

| Anggota | Tipe | Keterangan |
|---|---|---|
| `total_item` | Atribut kelas (publik) | Menghitung total objek `Item` yang pernah dibuat. Bertambah setiap kali `__init__` dipanggil. |
| `__base_price` | Atribut kelas (privat) | Harga dasar pengali harga, nilai awal `10`. Diakses lewat *name mangling* `_Item__base_price`. |
| `__price` | Atribut instance (privat) | Harga akhir item = `price` (input) dikali `__base_price` saat item dibuat. |
| `name` | Atribut instance | Nama item. |

**Konstruktor** `__init__(self, name, price)`
- Jika `price <= 0`, nilai dipaksa menjadi `10` (validasi sederhana agar harga tidak negatif/nol).
- Harga akhir dihitung sebagai `price * Item.__base_price` **pada saat objek dibuat** (bukan properti dinamis — perubahan `base_price` setelahnya tidak memengaruhi item yang sudah ada).
- Menambah `Item.total_item` sebanyak 1.

**Property `price`**
- *Getter*: mengembalikan `__price`.
- *Setter*: bersifat **inkremental**, yaitu `self.__price = max(0, self.__price + value)`. Artinya `item.price = 5` akan **menambah** 5 ke harga saat ini (bukan mengganti langsung), dan tidak boleh kurang dari 0.

**Class Method `base_price(cls, value)`**
- Mengubah `__base_price` secara inkremental (`+= value`), dengan batas bawah 0.
- Karena bersifat *class method*, perubahan ini berlaku secara global untuk kelas `Item` (memengaruhi item yang dibuat **setelah** pemanggilan ini).

**`__str__`**
- Format tampilan: `Nama: <name>\nHarga: <price>`.

### 2. `ItemStack`

Membungkus satu `Item` beserta jumlah tumpukannya (*stack*) di dalam inventaris  mirip slot item pada game yang bisa menampung banyak barang sejenis.

| Anggota | Tipe | Keterangan |
|---|---|---|
| `item` | Atribut instance | Objek `Item` yang ditumpuk. |
| `__stack` | Atribut instance (privat) | Jumlah item dalam tumpukan tersebut. |

**Property `stack`**
- *Getter*: mengembalikan `__stack`.
- *Setter*: inkremental seperti pada `Item.price` → `self.__stack = max(0, self.__stack + value)`, tidak boleh kurang dari 0.

**`__str__`**
- Menggabungkan representasi `Item` dengan baris tambahan `Tumpukan: <stack>`.

### 3. `Inventory`

Mengelola kumpulan `ItemStack` milik seorang karakter, dengan kapasitas slot terbatas.

| Anggota | Tipe | Keterangan |
|---|---|---|
| `max_slot` | Atribut kelas | Kapasitas maksimum slot inventaris (default `10`), sama untuk semua objek `Inventory`. |
| `__slot` | Atribut instance (privat) | Disalin dari `max_slot` saat inventaris dibuat. |
| `list_item` | Atribut instance | List berisi objek `ItemStack`. |

**`add_item(self, item: ItemStack)`**
- Jika `item`  sudah ada di `list_item`, jumlah stack-nya ditambahkan ke entri yang sudah ada.
- Jika belum ada dan slot masih tersedia (`len(list_item) < __slot`), item baru ditambahkan ke list.
- Jika slot penuh, mencetak pesan `"Maaf, Inventaris Penuh"`.

**`delete_item_from_inventory(self)`**
- Menghapus item di inventory yang memiliki stack 0

**`show_list_item(self)`**
- Mencetak seluruh item dalam inventaris menggunakan `__str__` masing-masing `ItemStack`.

### 4. `Character`

Cetak biru karakter pemain, memiliki nama, emas (*gold*), dan invenstaris sendiri.

| Anggota | Tipe | Keterangan |
|---|---|---|
| `name` | Atribut instance | Nama karakter (divalidasi saat pembuatan). |
| `__gold` | Atribut instance (privat) | Jumlah emas yang dimiliki, awal `0`. |
| `inventory` | Atribut instance | Objek `Inventory` baru, unik untuk tiap karakter. |

**Konstruktor `__init__(self, name)`**
- Memanggil `name_validation(name)`; jika `False`, melempar `ValueError("Nama tidak boleh mengandung angka")`.
- Jika valid, `name` disimpan dan `Inventory` baru dibuat.

**Property `gold`**
- *Getter*: mengembalikan `__gold`.
- *Setter*: inkremental & tidak boleh negatif → `self.__gold = max(0, self.__gold + value)`.

**Static Method `name_validation(name)`**
- Mengembalikan `True` jika `name` adalah `str` dan seluruhnya berupa huruf (`str.isalpha()` — tidak mengandung angka, spasi, atau simbol).
- Dipanggil tanpa perlu instance (`Character.name_validation(...)`).

## Alur Program (`main`)

Blok `if __name__ == "__main__":` menjalankan skenario pengujian berurutan:

1. **Uji Class Method** akan memanggil `Item.base_price(15)`, sehingga `__base_price` naik dari `10` menjadi `25`.
2. **Uji Objek** — akan membuat dua `Item` (`Cangkul Besi` harga input `2`, `Potion Merah` harga input `1`) dan dua `ItemStack`, lalu dua `Character` (`Arthur`, `Merlin`).
3. **Uji Instance Method**  menambahkan `stack1` dan `stack2` ke inventaris Arthur, lalu menambahkan `stack2` sekali lagi untuk menguji penggabungan stack pada item yang sama.
4. **Uji Setter** akan melakukkan pengujian pada setter `gold` dan `stack` dengan nilai positif lalu nilai negatif besar untuk memastikan hasil tertahan (*clamped*) di angka `0`.
5. **Uji Hapus Item** mengurangi `stack1` hingga `0`, lalu memanggil `delete_item_from_inventory()` untuk memastikan item dengan stack `0` terhapus dari daftar.
6. **Uji Static Method** akan memanggil `Character.name_validation("Lancelot")` dan mencoba membuat `Character("akbar123")` untuk menguji penanganan `ValueError`.

## Panduan Pengujian

### Cara Menjalankan

```bash
python3 main.py
```

Menggunakan Python standar (disarankan Python 3.14+) atau yang lebih baru tanpa modul external.

### Uji Manual

Jika ingin melakukan pengujian lebih  lanjut, berikut beberapa hal yang dapat di coba:

- **Inventaris penuh**: tambahkan lebih dari `Inventory.max_slot` (10) jenis item berbeda ke satu inventaris, lalu pastikan pesan `"Maaf, Inventaris Penuh"` muncul saat slot ke-11 ditambahkan.
- **Perubahan `base_price` di tengah permainan**: buat satu `Item` sebelum dan satu lagi sesudah memanggil `Item.base_price(...)`, lalu bandingkan harga keduanya untuk memverifikasi bahwa harga hanya dihitung sekali saat objek dibuat.
