# -*- encoding: utf-8 -*-
from constantes import *
from gestorRecursos import *

class listaVidas:
    def __init__(self):
        self.listaVidas = []
        
        posicionVertical = 115
        for i in range(1,10):
            posicionVertical += 30
            self.listaVidas.append(Vida(posicionVertical))
    
    def dibujar(self,pantalla):
        for vida in self.listaVidas:
            vida.dibujar(pantalla)
    
    def perderVida(self):
        listaVidas.pop()
    
class Vida:
    def __init__ (self,x):
        self.imagen = GestorRecursos.CargarImagen('Vida/Vida.png', -1)
        self.rect = self.imagen.get_rect()
        self.rect.bottom = ALTO_PANTALLA
    
        # La subimagen que estamos viendo
        self.rectSubimagen = pygame.Rect(0, 0, ANCHO_PANTALLA, ALTO_PANTALLA)
        self.establecerPosicion((x,80))
    
    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, self.rect, self.rectSubimagen)	
    
    def establecerPosicion(self, posicion):
        (posicionx, posiciony) = posicion
        self.rect.left = posicionx
        self.rect.bottom = posiciony    