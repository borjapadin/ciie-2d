# -*- encoding: utf-8 -*-
from constantes import *
from gestorRecursos import *
from elementosDibujables import *

class Inventario(ElementosDibujables):
        def __init__ (self):
                self.listObjetos = []
                nombreListaObjetos = ['bidonGasolinaSinConseguir','llaveSinConseguir']
                posicionVertical = 600
                for i in range(0,2):
                        posicionVertical += 35
                        self.listObjetos.append(ObjetoInventario(i+1,nombreListaObjetos[i]))                
    
        def dibujar(self, pantalla):
                for objeto in self.listObjetos:
                        objeto.dibujar(pantalla)  
    
        def guardarObjeto(self,objetoInventario):
                self.listObjetos.append(objetoInventario)


class ObjetoInventario:
        def __init__(self,numInventario,imagen):
                self.x = (numInventario*35)+600 #El número de inventario determina la posicion
                self.cargarImagen(imagen)
                self.numInventario = numInventario
        
        def dibujar(self, pantalla):
                pantalla.blit(self.imagen, self.rect, self.rectSubimagen)
                
        def numObjeto(self):
                return self.numInventario
        
        def cargarImagen(self, imagenInventario):        
                objetoVidaImagen = 'Inventario/' + imagenInventario + '.png'
                self.imagen = GestorRecursos.CargarImagen(objetoVidaImagen, -1)
                self.rect = self.imagen.get_rect()
                self.rect.bottom = ALTO_PANTALLA

                # La subimagen que estamos viendo
                self.rectSubimagen = pygame.Rect(0, 0, ANCHO_PANTALLA, ALTO_PANTALLA)
                self.establecerPosicion((self.x,165))     
                
        def establecerPosicion(self, posicion):
                (posicionx, posiciony) = posicion
                self.rect.left = posicionx
                self.rect.bottom = posiciony   
        
        def update(self):
                self.imagen = GestorRecursos.CargarImagen('Inventario/bidonGasolina.png', -1)
        
    