
# -*- encoding: utf-8 -*-
import pygame
#import pyganim (?)
from pygame.locals import *
from gestorRecursos import *
from escena import *
from director import *
from ElementoGUI import *
#Clase TextoGUI y los distintos textos

class  TextoGUI(ElementoGUI):
    def __init__(self, pantalla, fuente, color, texto, posicion):
        #Se crea la imagen del texto
        self.imagen = fuente.render(texto, True, color)
        #Se llama al método de la clase padre con el rectángulo que ocupa el texto
        ElementoGUI.__init__(self, pantalla, self.imagen.get_rect())
        #Se coloca el rectangulo en su posicion
        self.establecerPosicion(posicion)

    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, self.rect)
    
    
    
    
    