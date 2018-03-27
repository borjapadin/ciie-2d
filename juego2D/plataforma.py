# -*- encoding: utf-8 -*-
import pygame
import sys
import os
import time
from pygame.locals import *
from escena import *
from gestorRecursos import *
from random import randint
from personajes import *

# -------------------------------------------------
# Clase Plataforma


class Plataforma(MiSprite):

    def __init__(self, rectangulo):
        # Primero invocamos al constructor de la clase padre
        MiSprite.__init__(self)
        # Rectangulo con las coordenadas en pantalla que ocupara
        self.rect = rectangulo
        # Y lo situamos de forma global en esas coordenadas
        self.establecerPosicion((self.rect.left, self.rect.bottom))
        # En el caso particular de este juego, las plataformas no se van a ver,
        # asi que no se carga ninguna imagen
        self.image = pygame.Surface((0, 0))


     
    
