# -*- encoding: utf-8 -*-
import pygame
#import pyganim (?)
from pygame.locals import *
from gestorRecursos import *
from escena import *
from director import *
from elementoGUI import *


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
      

class TextoJugar(TextoGUI):
    def __init__(self, pantalla):
        # La fuente la debería cargar el estor de recursos
        fuente = pygame.font.SysFont('impact', 30);
        TextoGUI.__init__(self, pantalla, fuente, BLANCO, 'Empezar partida', (75, 395))
    def accion(self):
        self.pantalla.menu.ejecutarJuego()


class TextoSalir(TextoGUI):
    def __init__(self, pantalla):
        # La fuente la debería cargar el estor de recursos
        fuente = pygame.font.SysFont('impact', 30);
        TextoGUI.__init__(self, pantalla, fuente, BLANCO, 'Salir', (75, 445))


class TextoContinuar(TextoGUI):
    def __init__(self, pantalla):
        # La fuente la debería cargar el estor de recursos
        fuente = pygame.font.SysFont('impact', 30);
        TextoGUI.__init__(self, pantalla, fuente, BLANCO, 'Continuar', (120, 495))


class TextoVolverJuego(TextoGUI):
    def __init__(self, pantalla):
        # La fuente la debería cargar el estor de recursos
        fuente = pygame.font.SysFont('impact', 30);
        TextoGUI.__init__(self, pantalla, fuente, BLANCO, 'Volver a jugar', (75, 500))


class TextoTituloNivel(TextoGUI):
    def __init__(self, pantalla, nombreFase):
        # La fuente la debería cargar el estor de recursos
        fuente = pygame.font.SysFont('impact', 50);
        TextoGUI.__init__(self, pantalla, fuente, BLANCO, 'Nivel '+nombreFase, (100, 250))

class TextoNivel(TextoGUI):
    def __init__(self, pantalla, nombreFase, coordenada):
        fuente = pygame.font.SysFont('impact', 30);
        TextoGUI.__init__(self, pantalla, fuente, BLANCO, nombreFase, (40, coordenada))
