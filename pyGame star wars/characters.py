class Lokasyon:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def setX(self, yeniX: int):
        self.x = yeniX

    def setY(self, yeniY: int):
        self.y = yeniY


class Karakter:
    def __init__(self, ad: str, tur: str, konum: Lokasyon):
        self.ad = ad
        self.tur = tur  
        self.konum = konum

    def getAd(self):
        return self.ad

    def setAd(self, yeniAd: str):
        self.ad = yeniAd

    def getTur(self):
        return self.tur

    def setTur(self, yeniTur: str):
        self.tur = yeniTur

    def getKonum(self):
        return self.konum

    def setKonum(self, yeniKonum: Lokasyon):
        self.konum = yeniKonum

    def EnKisaYol(self):
        raise NotImplementedError("Bu metod alt sınıflarda ezilmelidir.")


class IyiKarakter(Karakter):
    def __init__(self, ad: str, konum: Lokasyon, can: int):
        super().__init__(ad, "İyi", konum)
        self.can = can

    def getCan(self):
        return self.can

    def setCan(self, yeniCan: int):
        self.can = yeniCan


class MasterYoda(IyiKarakter):
    def __init__(self, konum: Lokasyon):
        super().__init__("Master Yoda", konum, 3)  

    def yakalanma(self):
        self.can = max(0, self.can - 0.5)  


class LukeSkywalker(IyiKarakter):
    def __init__(self, konum: Lokasyon):
        super().__init__("Luke Skywalker", konum, 3)

    def yakalanma(self):
        self.can -= 1


class KotuKarakter(Karakter):
    def __init__(self, ad: str, konum: Lokasyon):
        super().__init__(ad, "Kötü", konum)

    def EnKisaYol(self, grid, target_pos):
        raise NotImplementedError("Bu metod alt sınıflarda ezilmelidir.")


class DarthVader(KotuKarakter):
    def __init__(self, konum: Lokasyon):
        super().__init__("Darth Vader", konum)

    def EnKisaYol(self, grid, target_pos):
        
        from utils import darth_vader_shortest_path
        start = (self.konum.getX(), self.konum.getY())
        end = (target_pos.getX(), target_pos.getY())
        return darth_vader_shortest_path(grid, start, end)


class KyloRen(KotuKarakter):
    def __init__(self, konum: Lokasyon):
        super().__init__("Kylo Ren", konum)

    def EnKisaYol(self, grid, target_pos):
        
        from utils import bfs_shortest_path
        start = (self.konum.getX(), self.konum.getY())
        end = (target_pos.getX(), target_pos.getY())
        return bfs_shortest_path(grid, start, end)


class Stormtrooper(KotuKarakter):
    def __init__(self, konum: Lokasyon):
        super().__init__("Stormtrooper", konum)

    def EnKisaYol(self, grid, target_pos):
        
        from utils import bfs_shortest_path
        start = (self.konum.getX(), self.konum.getY())
        end = (target_pos.getX(), target_pos.getY())
        return bfs_shortest_path(grid, start, end)