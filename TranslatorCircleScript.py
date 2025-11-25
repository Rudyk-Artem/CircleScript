from BasicTypes import *
from BasicFunctions import *

path=input("Шлях до файлу з кодом: ")
with open(path,'r') as file:
    info=file.read()
print(info)

#буде зроблено після BasicTypes і BasicFunctions