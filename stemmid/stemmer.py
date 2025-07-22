from more_itertools import flatten              
from functools import cache
from copy import copy
from pathlib import Path

import re

class Stemmer(object) :

    def _longest_str(self, lst: list[str]) -> str:
        return max((s for s in lst if isinstance(s, str)), key=len, default=None)

    def _load_dict(self, inc, exc) :
        try :
            with open(Path(__file__).parent / 'data' / 'kd.txt', "r") as file :
                kamus_dasar = {
                    kt for kt
                    in file.read().split("\n")
                    if kt not in exc
                }
            if inc :
                for da in inc :
                    kamus_dasar.add(da)            
            return kamus_dasar
        except FileNotFoundError :
            print("Kamus gagal di muat!")

    def __init__(self,
        with_lemmatization: bool = True,
        inc:list[str] = [],
        exc:list[str] = []
    ):
        self.with_lemmatization = with_lemmatization
        self.katas = self._load_dict(inc, exc)
        self.lemmatization_rules =  {
            "m" : {"p"},
            "n" : {"t"},
            "ny" : {"c", "s"},
            "ng" : {""},
            "nge" : {""},
        }

    def is_on_there(self, kata) :
        return kata in self.katas

    @cache
    def lemmatization(self, kata:str) -> str | None :
        if self.is_on_there(kata) :
            return None
        for mono in [(kata.startswith(str(x)), x) for x in self.lemmatization_rules.keys()] :
            if mono[0] :
                for gibran in self.lemmatization_rules[mono[1]] :
                    anies = kata.replace(mono[1], gibran, 1)
                    if self.is_on_there(anies) :
                        return anies
                    continue
        return None        
      
    def _match1(self, kata: str, prefix: str, suffix: str) :
        """
        Mencoba mencocokkan string `kata` terhadap awalan dari setiap kata dalam string `prefix`.
        
        Fungsi ini adalah bagian dari sistem pencocokan berbasis kata yang melibatkan:
        - Pengecekan apakah `kata` sudah ada dalam konteks tertentu (`is_on_there`).
        - Pencocokan awalan `kata` terhadap setiap kata dalam `curse`.
        - Pemrosesan sisa string (`jadi`) jika ada kecocokan awalan.
        - Lematisasi kata untuk mendapatkan bentuk dasar.
        - Pemanggilan fungsi fallback `_match2` jika pencocokan tidak berhasil.

        Parameter:
        ----------
        kata : str
            Kata yang akan diperiksa dan dicocokkan.
        prefix : str
            String berisi satu atau lebih kata yang akan dibandingkan terhadap awalan `kata`.
        suffix : 
            Parameter yang akan diteruskan ke fungsi `_match2` sebagai fallback jika pencocokan gagal.

        Yields:
        -------
        str atau hasil dari self._match2
            Mengembalikan hasil pencocokan berupa string sisa (`jadi`), hasil lematisasi, 
            atau hasil dari fungsi `_match2` jika tidak ada kecocokan.
        """

        if self.is_on_there(kata) :
            yield kata
            return
        lowres = [(kata.startswith(x), x) for x in prefix.split(" ")]
        joko = copy(kata)
        for lo in lowres :
            lemm = (
                self.lemmatization(joko)
                if self.with_lemmatization 
                else joko
            )
            jadi = kata[len(lo[1]) :]
            joko = copy(jadi)
            if lo[0] :            
                yield (
                    jadi
                    if self.is_on_there(jadi)
                    else self._match2(kata, suffix)
                )                
            if lemm:
                yield lemm            
        if all([not lo[0] for lo in lowres]) :
            yield self._match2(kata, suffix)

    def _match2(self, kata, suffix: str) :
        """
        Mencoba mencocokkan string `kata` terhadap akhiran dari setiap kata dalam string `suffix`.

        Fungsi ini melakukan iterasi terhadap setiap kata dalam `suffix`, lalu:
        - Memeriksa apakah `kata` berakhiran salah satu dari kata dalam `suffix`.
        - Jika ya, menghilangkan bagian akhiran tersebut dari `kata` dan mengembalikannya.
        - Jika tidak, mengembalikan `kata` apa adanya.

        Parameter:
        ----------
        kata : str
            Kata yang akan diperiksa terhadap akhiran.
        suffix : str
            String yang berisi satu atau lebih kata yang akan dibandingkan sebagai akhiran dari `kata`.

        Yields:
        -------
        str
            Kata yang telah dihilangkan akhiran jika ada kecocokan, atau `kata` asli jika tidak cocok.
        """
        
        for lo in [(kata.endswith(y), y) for y in suffix.split(" ")] :
            if lo[0]:
                yield kata[: - len(lo[1])]
            else :
                yield kata
        
    @cache        
    def _jika(self, kata) -> tuple[list, list]:
        """
        Melakukan proses analisis terhadap kemungkinan bentuk dasar dari sebuah kata
        dengan menghapus awalan dan akhiran menggunakan fungsi `_match1`.

        Fungsi ini dioptimalkan untuk menghindari konflik antar prefix/suffix dengan
        cara memproses daftar awalan dan akhiran secara terstruktur.

        Langkah utama:
        1. Memanggil `_match1` dengan daftar awalan dan akhiran untuk menghasilkan 
           variasi bentuk kata.
        2. Menyimpan hasil dalam struktur nested list (`super`) dan diratakan (`flatten`).
        3. Jika hasil ditemukan dalam kamus (`is_on_there`), dimasukkan ke `hasil`.
        4. Sisanya dimasukkan ke dalam `jyahh` sebagai alternatif yang belum dikenali.

        Parameter:
        ----------
        kata : str
            Kata yang akan dianalisis untuk menemukan kemungkinan bentuk dasarnya.

        Returns:
        --------
        tuple[list, list]
            - `hasil`: List dari bentuk dasar yang dikenali.
            - `jyahh`: Set dari bentuk kata alternatif yang tidak dikenali (hasil gagal lemmatization).
        """

        jyahh = set()
        hasil = []
        super = []
        for ka in self._match1(
            kata,
            prefix = "me di ng ny mem per pen peng men se ber ke ter meng memper", 
            suffix = "kan annya an i in hkan kah nya inya mu ku lah kannya"
        ) :
            if isinstance(ka, str) :
                super.append([ka])
                continue
            super.append(ka)
        for deuh in flatten(super) :
            if self.is_on_there(deuh) :
                hasil.append(deuh)
                break
            else :
                jyahh.add(deuh)
        return hasil, jyahh        

    @cache
    def load(self, kata: str) -> str:
        """
        Mencari bentuk dasar (lemma) dari sebuah kata dengan pendekatan bertingkat (termasuk pemaksaan jika perlu).

        Proses utama:
        1. Memanggil `_jika` untuk mencari bentuk dasar (`hasil`) dan bentuk alternatif yang gagal (`gagal`).
        2. Jika tidak ditemukan hasil dari tahap pertama, mencoba lagi secara rekursif terhadap item di `gagal`.
        3. Jika ditemukan lebih dari satu hasil, memilih hasil dengan panjang string terpanjang menggunakan `_longest_str`.
        4. Jika semua gagal, mengembalikan kata aslinya.

        Pendekatan ini bersifat "memaksa", dalam arti mencoba segala kemungkinan untuk menemukan bentuk dasar.

        Parameter:
        ----------
        kata : str
            Kata yang akan diproses untuk menemukan bentuk dasarnya.

        Returns:
        --------
        str
            Bentuk dasar dari kata jika berhasil ditemukan, atau `kata` asli jika tidak ditemukan.
        """

        hasil, gagal = self._jika(kata)
        if not hasil  :
            for g in gagal :
                la = self._jika(g)[0]
                if la :
                    hasil.append(la[0])
        if len(hasil) >= 1 :
            return self._longest_str(hasil)
        return kata

    def __start_stemming(self, kalimat: str) :
        return " ".join([self.load(y) for y in ' '.join(re.sub(r'[^\w]', ' ', kalimat.lower()).split()).split(" ")])

    def loads(self, kalimat: str) -> str:
        """
        Stemming dari kalimat.\n
        >>> Berbuat salahnya
        >>> buat salah
        """

        return self.__start_stemming(kalimat)
      