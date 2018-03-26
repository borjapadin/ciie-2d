# -*- encoding: utf-8 -*-
import pygame
from constantes import *


class Escena:
    def __init__(self, director):
        self.director = director

    def update(self, *args):
        raise NotImplemented("Tiene que implementar el metodo update.")

    def eventos(self, *args):
        raise NotImplemented("Tiene que implementar el metodo eventos.")

    def dibujar(self):
        raise NotImplemented("Tiene que implementar el metodo dibujar.")


class EscenaPygame(Escena):
    def __init__(self, director):
        Escena.__init__(self, director)
        # Inicializamos la libreria de pygame (si no esta inicializada ya)
        pygame.init()
        # Creamos la pantalla (si no esta creada ya)
        self.pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
