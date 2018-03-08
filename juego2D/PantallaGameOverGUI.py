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
    
        # Creamos los botones y los metemos en la lista
        self.botonJugar = BotonVolverJugar(self)
        self.botonSalir = BotonSalir(self)
    
        self.elementosGUI.append(self.botonJugar)
        self.eventoSeleccionado = "jugar"
        #  self.elementosGUI.append(botonSalir)
    
    def addBotonJugar(self):
        self.elementosGUI.pop()
        self.elementosGUI.append(self.botonJugar)
        self.eventoSeleccionado = "jugar"        
        
    def addBotonSalir(self):
        self.elementosGUI.pop()
        self.elementosGUI.append(self.botonSalir)
        self.eventoSeleccionado = "salir"   
    
    def eliminarUltimosDosElementos(self):
        self.elementosGUI.pop()
        self.elementosGUI.pop()

    #Sobreescribir
    def eventos(self, lista_eventos):
        for evento in lista_eventos:
            if evento.type == KEYDOWN: 
                #Aceptar acción
                if evento.key == K_RETURN: 
                    elemento = self.elementosGUI.pop()
                    elemento.accion()
                          
                #Cambiar de opción
                if evento.key == K_DOWN or evento.key == K_UP:
                    if self.eventoSeleccionado == "jugar":
                        self.addBotonSalir()
                    elif self.eventoSeleccionado == "salir":
                        self.addBotonJugar() 
                       
                if evento.type == pygame.QUIT: #EHHHHHHHHHHHHHHHHH... si?
                    self.director.salirPrograma()                     
    
        
class TextoJugar(TextoGUI):
    def __init__(self, pantalla):
        # La fuente la debería cargar el estor de recursos
        fuente = pygame.font.SysFont('impact', 30);
        TextoGUI.__init__(self, pantalla, fuente, (255, 255, 255), 'Empezar partida', (65, 395))
    def accion(self):
        self.pantalla.menu.ejecutarJuego()

class TextoSalir(TextoGUI):
    def __init__(self, pantalla):
        # La fuente la debería cargar el estor de recursos
        fuente = pygame.font.SysFont('impact', 30);
        TextoGUI.__init__(self, pantalla, fuente, (255, 255, 255), 'Salir', (65, 445))
    def accion(self):
        self.pantalla.menu.salirPrograma()
        
class BotonVolverJugar(Boton):
    def __init__(self, pantalla):
        Boton.__init__(self, pantalla, 'Menu/BotonGranada.png', (20,400))

    def accion(self):
        self.pantalla.menu.ejecutarJuego()

class BotonSalir(Boton):
    def __init__(self, pantalla):
        Boton.__init__(self, pantalla, 'Menu/BotonGranada.png', (20,450))

    def accion(self):
        self.pantalla.menu.salirPrograma()

