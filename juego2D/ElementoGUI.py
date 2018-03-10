# -*- encoding: utf-8 -*-
import pygame
#import pyganim (?)
from pygame.locals import *
from gestorRecursos import *
from escena import *
from director import *

#Clase abstracta ElementoGUI
class ElementoGUI:
    def __init__(self, pantalla, rectangulo):
        self.pantalla = pantalla
        self.rect = rectangulo

    #Método para situarlo en la pantalla
    def establecerPosicion(self, posicion):
        (posicionx, posiciony) = posicion
        self.rect.left = posicionx
        self.rect.bottom = posiciony

    #Te dice si se ha hecho clic en el
    def posicionEnElemento(self, posicion):
        (posicionx, posiciony) = posicion
        if (posicionx>=self.rect.left) and (posicionx<=self.rect.right) and (posiciony>=self.rect.top) and (posiciony<=self.rect.bottom):
            return True
        else:
            return False
        
    def devolverCenterX(self):
        return self.rect.centerx
   
    def moverIp(self):
        return self.rect.move_ip(-5, 0)  
    #Métodos abstractos
    def dibujar(self):
        raise NotImplemented("Tiene que implementar el metodo dibujar")

    def accion(self):
        raise NotImplemented("Tiene que implementar el metodo de accion")
