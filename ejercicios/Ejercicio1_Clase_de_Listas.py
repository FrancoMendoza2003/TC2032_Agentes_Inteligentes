#Franco Mendoza Muraira A01383399

class Lista:
    MAX = 100
    def __init__(self):
        self.data = [0] *self.MAX
        self.size = 0
    
    def insert(self,valor):
        if self.size < self.MAX:
            self.data[self.size] = valor
            self.size += 1

    def erase(self):
        if self.size > 0:
            self.size-=1
            return self.data[self.size]
        else:
            return "NO HAY ELEMENTOS"
    
    def getData(self,posicion):
        if 0 <= posicion < self.size:
            return self.data[posicion]
    
    def getSize(self):
        return self.size
    
    def print(self):
        for i in range(self.size):
            print(f"[{i}] - {self.data[i]}")


listilla = Lista()

listilla.insert(154)
listilla.insert(587)
listilla.insert(874)

listilla.print()
print("Tamaño de la lista:", listilla.getSize())
print("Elemento en la posición 1:", listilla.getData(1))

listilla.erase()
listilla.print()
listilla.erase()
print()
listilla.print()
listilla.erase()
listilla.print()





