# -*- encoding: utf-8 -*-
from constantes import *
from gestorRecursos import *
from elementosDibujables import *
# Clase Cielo: aún no tiene nada prácticamente, solo un background negro.

class Cielo(ElementoDibujable):
    def __init__(self,nombreFase):
        self.posicionx = 0 # El lado izquierdo de la subimagen que se esta visualizando
        self.update(0)

    def update(self, tiempo):
        # Calculamos el color del cielo
        self.colorCielo = NEGRO

    def dibujar(self,pantalla):
        # Dibujamos el color del cielo
        pantalla.fill(self.colorCielo)
        self.colorCielo = NEGRO

