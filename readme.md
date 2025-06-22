# Stemmid

Proyek ini adalah implementasi stemmer Bahasa Indonesia berbasis daftar kata dasar. Stemmer digunakan untuk mengubah kata berimbuhan menjadi bentuk dasarnya.

Perbedaan dengan PySastrawi Kode 100x lebih pendek dan lebih lambat 0.01mil detik. Tidak akan terjadi missmatch jika masih dalam lingkup antar kata.
<br>
### Initial
```python
>>> from stemmid import Stemmer
>>> Stemmer().load("menangis")
    "tangis"
```
### Menambah kata ke Kamus
```python
>>> Stemmer().load("belajarlah")
    "belajarlah"
>>> Stemmer(inc=["belajar"]).load("belajarlah")
    "belajar"
```
### Mengecualikan Kata
```python
>>> Stemmer().load("menyusui")
    "susu"
>>> Stemmer(exc=["susu"]).load("menyusui")
    "menyusui"
```
### Menggunakan Kalimat
```python
>>> Stemmer().loads("Kehilangan Permainan") 
    "hilang mainan"
```