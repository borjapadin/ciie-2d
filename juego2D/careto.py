# -*- encoding: utf-8 -*-
from constantes import *
from gestorRecursos import *

class Careto:
    def __init__ (self,nombreFase):
        self.imagen = GestorRecursos.CargarImagen('Fase'+nombreFase+'/Careto/careto.png', -1)
        self.rect = self.imagen.get_rect()
        self.rect.bottom = ALTO_PANTALLA
    
        # La subimagen que estamos viendo
        self.rectSubimagen = pygame.Rect(0, 0, ANCHO_PANTALLA, ALTO_PANTALLA)
        self.establecerPosicion((40,150))
        
    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, self.rect, self.rectSubimagen)	
    
    def establecerPosicion(self, posicion):
        (posicionx, posiciony) = posicion
        self.rect.left = posicionx
        self.rect.bottom = posiciony    