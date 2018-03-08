# -*- encoding: utf-8 -*-
import pygame
#import pyganim (?)
from pygame.locals import *
from gestorRecursos import *
from escena import *
from director import *
from fase import *
from PantallaGUI import *
from TextoGUI import *
from Boton import *

class PantallaInicialGUI(PantallaGUI):
    def __init__(self, menu):
        PantallaGUI.__init__(self, menu, 'Menu/PantallaInicio.jpg')

        # Creamos los botones y los metemos en la lista
        botonJugar = BotonJugar(self)
        botonSalir = BotonSalir(self)

        self.elementosGUI.append(botonJugar)
        self.elementosGUI.append(botonSalir)

        # Creamos el texto y lo metemos en la lista
        textoJugar = TextoJugar(self)
        textoSalir = TextoSalir(self)
        self.elementosGUI.append(textoJugar)
        self.elementosGUI.append(textoSalir)

class TextoJugar(TextoGUI):
    def __init__(self, pantalla):
        # La fuente la debería cargar el estor de recursos
        fuente = pygame.font.SysFont('impact', 30);
        TextoGUI.__init__(self, pantalla, fuente, (255, 255, 255), 'Empezar partida', (60, 395))
    def accion(self):
        self.pantalla.menu.ejecutarJuego()

class TextoSalir(TextoGUI):
    def __init__(self, pantalla):
        # La fuente la debería cargar el estor de recursos
        fuente = pygame.font.SysFont('impact', 30);
        TextoGUI.__init__(self, pantalla, fuente, (255, 255, 255), 'Salir', (60, 445))
    def accion(self):
        self.pantalla.menu.salirPrograma()
        
class BotonJugar(Boton):
    def __init__(self, pantalla):
        Boton.__init__(self, pantalla, 'Menu/BotonGranada.png', (20,400))

    def accion(self):
        self.pantalla.menu.ejecutarJuego()

class BotonSalir(Boton):
    def __init__(self, pantalla):
        Boton.__init__(self, pantalla, 'Menu/BotonGranada.png', (20,450))

    def accion(self):
        self.pantalla.menu.salirPrograma()