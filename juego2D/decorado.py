# -*- encoding: utf-8 -*-
from constantes import *
from gestorRecursos import *
from ElementosDibujables import *
# -------------------------------------------------
# Clase Decorado

class Decorado(ElementoDibujable):
    def __init__(self,nombreFase):
        self.imagen = GestorRecursos.CargarImagen('Fase'+nombreFase+'/decorado.png', -1)
        self.imagen = pygame.transform.scale(self.imagen, (1200, 400))

        self.rect = self.imagen.get_rect()
        self.rect.bottom = ALTO_PANTALLA

        # La subimagen que estamos viendo
        self.rectSubimagen = pygame.Rect(0, 0, ANCHO_PANTALLA, ALTO_PANTALLA)
        self.rectSubimagen.left = 0 # El scroll horizontal empieza en la posicion 0 por defecto

    def update(self, scrollx):
        self.rectSubimagen.left = scrollx

    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, self.rect, self.rectSubimagen)

