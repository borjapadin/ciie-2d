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

class PantallaGameOverGUI(PantallaGUI):
    def __init__(self, menu):
        PantallaGUI.__init__(self, menu, 'Menu/PantallaGameOver_2.jpg')
        
        # Creamos el texto y lo metemos en la lista
        textoSalir = TextoSalir(self)
        self.elementosGUI.append(textoSalir) 
        
        self.botonSalir = BotonSalir(self)   
        self.elementosGUI.append(self.botonSalir)        

    #Sobreescribir
    def eventos(self, lista_eventos):
        for evento in lista_eventos:
            if evento.type == KEYDOWN: 
                #Aceptar acción
                if evento.key == K_RETURN: 
                    elemento = self.elementosGUI.pop()
                    elemento.accion()
                       
                if evento.type == pygame.QUIT: #EHHHHHHHHHHHHHHHHH... si?
                    self.director.salirPrograma()                     


class TextoSalir(TextoGUI):
    def __init__(self, pantalla):
        # La fuente la debería cargar el estor de recursos
        fuente = pygame.font.SysFont('impact', 30);
        TextoGUI.__init__(self, pantalla, fuente, (255, 255, 255), 'Salir', (65, 445))
    def accion(self):
        self.pantalla.menu.salirPrograma()


class BotonSalir(Boton):
    def __init__(self, pantalla):
        Boton.__init__(self, pantalla, 'Menu/BotonGranada.png', (20,450))

    def accion(self):
        self.pantalla.menu.salirPrograma()

