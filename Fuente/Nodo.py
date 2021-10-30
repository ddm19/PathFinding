#Daniel domenech moreno - ddm19 - 54207039H
from casilla import *
import math

class Nodo:
 #-------------- Constructor ------------------
    def __init__ (self,x,y,padre,coste):
        self.x = x
        self.y = y
        self.padre = padre
        self.coste = coste
        self.f = 0
        self.g = 0
 #-------------- Getters ------------------
    def GetX(self):    
        return self.x
    def GetY(self):
        return self.y
    def GetPosi(self):
        return Casilla(self.x,self.y)
    def GetPadre(self):
        return self.padre
    def GetCoste(self):
        return self.coste
    def Getg(self):
        return self.g
    def Getf(self):
        return self.f
    def Geth(self):    # return 0 = Algoritmo sin Conocimiento (Búsqueda en Anchura)
        return 0
    @staticmethod
    def Manhattan(c1,c2): # Heurística Manhattan
        return abs(c2.getFila()-c1.getFila())+abs(c2.getCol()-c1.getCol())
    @staticmethod
    def Euclidea(c1,c2): # Heurística Euclídea
        return math.sqrt(pow(c2.getFila()-c1.getFila(),2)+pow(c2.getCol()-c1.getCol(),2))
    @staticmethod
    def DistanciaDiagonal(c1,c2): # Distancia Diagonal
        dx = abs(c1.getFila() - c2.getFila())
        dy = abs(c1.getCol() - c2.getCol())
        return ((dx + dy) + (1.5 - 2 * 1) * min(dx, dy))
 #-------------- Setters ------------------
    def SetCoste(self,newcoste):
        self.coste = newcoste
    def SetX(self,newx):
        self.x = newx
    def SetY(self,newy):
        self.y = newy
    def SetPadre(self,newpadre):
        self.padre = newpadre
    def SetF(self): # h = 0
        self.f = self.Getg()+self.Geth()
    def SetFMan(self,obj): # Manhattan
        self.f = self.Getg()+self.Manhattan(self.GetPosi(),obj)
    def SetFEucl(self,obj): # Euclídea
        self.f = self.Getg()+self.Euclidea(self.GetPosi(),obj)
    def SetFDDiag(self,obj): # Distancia Diagonal
        self.f = self.Getg()+self.DistanciaDiagonal(self.GetPosi(),obj)
#---------------- Métodos ---------------
    @staticmethod
    def CalculaCoste(m,n):
        coste = 1.0
        if m.getFila() != n.getFila() and m.getCol() != n.getCol(): # Movimiento diagonal
            coste = 1.5
            
        return coste
    def __lt__(self, other):
        return self.Getf() > other.Getf()