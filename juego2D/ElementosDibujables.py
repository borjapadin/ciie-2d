# -*- encoding: utf-8 -*-
from constantes import *
from gestorRecursos import *

class ElementosDibujables:
    def __init__ (self):
        self.elementosDibujables = []
    
    def agregarElemento(self,elementoDibujable):
        self.elementosDibujables.append(elementoDibujable)
    
    def agregarElementos(self,elementosDibujable):
        for elementoDibujable in iter(elementosDibujable):
            self.elementosDibujables.append(elementoDibujable)
    def dibujar(self,pantalla):
        for elementoDibujable in iter(self.elementosDibujables):
            elementoDibujable.dibujar(pantalla)
        
        
class ElementoDibujable:
    def dibujar(self, pantalla):
        raise NotImplemented("Tiene que implementar el metodo update.")    
    