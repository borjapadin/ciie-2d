# -*- encoding: utf-8 -*-
import pygame
#import pyganim (?)
from pygame.locals import *
from gestorRecursos import *
from escena import *
from director import *
from ElementoGUI import *

#Clase Boton con los correspondientes botones
class BotonNada(ElementoGUI):
    def __init__(self, pantalla, nombreImagen, posicion):
        #Se carga la imagen del boton
        self.imagen = GestorRecursos.CargarImagen(nombreImagen,-1)
        self.imagen = pygame.transform.scale(self.imagen,(45,45))
        #Se llama al ´método de la clase padre con el rectángulo que ocupa el botón
        ElementoGUI.__init__(self, pantalla, self.imagen.get_rect())
        #Se coloca el rectángulo en su posición
        self.establecerPosicion(posicion)

    def dibujar(self,pantalla):
        pantalla.blit(self.imagen,self.rect)