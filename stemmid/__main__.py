from stemmid import Stemmer
from sys import argv

model = Stemmer()
print(
    model.loads(argv[1])
)