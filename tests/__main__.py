import stemmid
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory as SF
from time import time
import unittest

class TestStringMethods(unittest.TestCase):
    def setUp(self):
        stem2 = stemmid.Stemmer()
        stemmer = SF().create_stemmer()
        self.sastrawi = lambda x : stemmer.stem(x)
        self.sastrawi2 = lambda x : stem2.loads(x)

        self.compare = lambda x : self.assertEqual(stem2.load(x), self.sastrawi(x))
        self.honorable = lambda x, y : self.assertEqual(stem2.loads(x), y)
        with open("tests/data/undangUndang.txt", "r", encoding="utf-8") as file :
            self.text = file.read()
    
    def test_prefix(self):
        self.compare("beradab")
        self.compare("berburu")
        self.compare("bersama")
        self.compare("bercinta")
        self.compare("dipamer")
        self.compare("diajak")
        self.compare("dicium")
        self.compare("memakan")
        self.compare("membenci")
        self.compare("mencari")
        self.compare("merakyat")
        self.compare("menjilat")
        self.compare("meludah")
        self.compare("perdalam")

    def test_sufix(self):
        self.compare("bangunkan")
        self.compare("makanan")
        self.compare("minuman")
        self.compare("sayangi")
        self.compare("benci")
        self.compare("tulisan")
        self.compare("lukisan")
        self.compare("bentukan")
        self.compare("berikan")
        self.compare("cintai")
        self.compare("hormati")
        self.compare("buktikan")
        self.compare("kerjakan")
        self.compare("mainkan")
        self.compare("tunjukkan")
        self.compare("pakaiannya")
        self.compare("tumbuhkan")
        self.compare("kembangkan")
        self.compare("sucikan")
        self.compare("terangkan")
        self.compare("tuliskannya")
        self.compare("bacakan")
        self.compare("dengarkan")
        self.compare("panjangkan")

    def test_full(self):
        self.compare("kekasihmu")
        self.compare("kematian")
        self.compare("keberanian")
        self.compare("pertandingan")
        self.compare("pendidikan")
        self.compare("kebencian")
        self.compare("kegagalan")
        self.compare("kesedihan")
        self.compare("memusnahkan")
        self.compare("kebakaran")
        self.compare("meminumnya")
        self.compare("membencinya")
        self.compare("kemerdekaan")
        self.compare("menafkahinya")
        self.compare("kekayaannya")
        self.compare("memperbudaknya")
        self.compare("menjilatinya")
        self.compare("mencucinya")
        self.compare("permainan")
        self.compare("kehilangan")

    def test_lemmatization(self):
        self.compare("menyalin")
        self.compare("menangisinya")
        self.compare("menyuruh")
        self.compare("mengopi")
        self.compare("menagih")
        self.compare("menyekolahi")
        self.compare("menyumbang")
        self.compare("penyakitnya")
        self.compare("menyumbanginya")
        self.compare("menolonginya")
        self.compare("meniru")

    # Sastrawi gabisa
    def test_honorable(self):
        self.honorable("benarin", "benar")
        self.honorable("menghisapnya", "hisap")
        self.honorable("bersholawat", "sholawat")
        self.honorable("menyubit", "cubit")
        self.honorable("nolong", "tolong")
        self.honorable("pelajari", "pelajar")
        self.honorable("menikah", "nikah")


    def test_time(self):
        kalimat = self.text*1
        asd = time()
        self.sastrawi2(kalimat)
        p_s = time() - asd
        print(f"time = {p_s:.5f}")

if __name__ == '__main__':
    unittest.main()