# -*- encoding: utf-8 -*-
from constantes import *
from gestorRecursos import *

class Inventario:
        def __init__ (self):
                self.listObjetos = []
    
        def dibujar(self, pantalla):
                for objeto in self.listObjetos:
                        objeto.dibujar(pantalla)  
    
        def guardarObjeto(self,objetoInventario):
                self.listaObjetos.add(objetoInventario)

class ObjetoInventario:
        def __init__(self,imagen):
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
                
    