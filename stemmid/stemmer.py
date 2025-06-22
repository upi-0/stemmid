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

    def __init__(self, inc:list[str] = [], exc:list[str] = []):
        self.katas = self._load_dict(inc, exc)

    def is_on_there(self, kata) :
        return kata in self.katas

    @property
    def lemmatization_rules(self) :
        return {
            "m" : {"p"},
            "n" : {"t"},
            "ny" : {"c", "s"},
            "ng" : {"k"},
            "nge" : {""},
        }

    @cache
    def lemmatization(self, kata:str) -> tuple[bool, str] :
        if self.is_on_there(kata) :
            return False, ""
        for mono in [(kata.startswith(str(x)), x) for x in self.lemmatization_rules.keys()] :
            if mono[0] :
                for gibran in self.lemmatization_rules[mono[1]] :
                    anies = kata.replace(mono[1], gibran, 1)
                    if self.is_on_there(anies) :
                        return True, anies
                    continue
        return False, ""              
      
    def _match1(self, kata: str, curse: str, callback_params: list) :
        if self.is_on_there(kata) :
            yield kata
            return
        lowres = [(kata.startswith(x), x) for x in curse.split(" ")]
        joko = copy(kata)
        for lo in lowres :
            lemm = self.lemmatization(joko)
            jadi = kata[len(lo[1]) :]
            joko = copy(jadi)
            if lo[0] :            
                yield (
                    jadi
                    if self.is_on_there(jadi)
                    else self._match2(*callback_params)
                )                
            if lemm[0] :
                yield lemm[1]                
        if all([not lo[0] for lo in lowres]) :
            yield self._match2(*callback_params)

    def _match2(self, kata, curse: str) :
        for lo in [(kata.endswith(y), y) for y in curse.split(" ")] :
            if lo[0] == True :
                yield kata[: - len(lo[1])]
            else :
                yield kata
        
    def _jika(self, kata) -> tuple[list, list]:
        jyahh = []
        hasil = []
        super = []

        """
        Paramater ini sudah di optimalkan sedemikian rupa agar tidak terjadi konflik antar Suffix/Prefix
        """
        for ka in self._match1(
            kata, "me di ng ny mem per pen men se ber ke ter meng memper", 
            [kata, "kan annya an i in hkan kah nya inya mu ku lah kannya"]
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
                jyahh.append(deuh)
        return hasil, jyahh        

    @cache
    def load(self, kata: str) -> str:
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
      