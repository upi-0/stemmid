# Stemmid

Proyek ini adalah implementasi stemmer Bahasa Indonesia berbasis daftar kata dasar. Stemmer digunakan untuk mengubah kata berimbuhan menjadi bentuk dasarnya.

Perbedaan dengan [PySastrawi](https://github.com/har07/PySastrawi):
- Source Code 100x lebih pendek.
- Algoritma yang digunakan berbeda.
- Lebih cepat hingga 10%.
- Kustomisasi kamus yang lebih uwaw.

## Install
```bash
pip install git+https://github.com/Malykz/stemmid
```
## How To user
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

## Test
Test dengan 1825 kata :
- sastrawi = 0.03424
- stemmid  = 0.02081

Test 1.825.000 kata (Cache) :
- sastrawi = 1.20500
- stemmid  = 0.97979
