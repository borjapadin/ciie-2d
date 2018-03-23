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
from Constantes import *

class PantallaCutSceneGUI(PantallaGUI):
    def __init__(self, menu):
        PantallaGUI.__init__(self, menu, 'Menu/CutScene/PantallaSiguienteNivel.png')
        
        # Creamos el texto y lo metemos en la lista
        textoSalir = TextoSalir(self)
        self.elementosGUI.append(textoSalir) 
        textoContinuar = TextoContinuar(self)
        self.elementosGUI.append(textoContinuar)
        
        #Creamos los botones
        self.botonSalir = BotonSalir(self)      
        self.botonContinuar = BotonContinuar(self)
        #Agregamos solo el que va a estar seleccionado la primera vez que se cree
        self.addBotonContinuar()
    
    def addBotonContinuar(self):
        self.elementosGUI.append(self.botonContinuar)
        self.eventoSeleccionado = "continuar"        
        
    def addBotonSalir(self):
        self.elementosGUI.append(self.botonSalir)
        self.eventoSeleccionado = "salir"   
    
    #Sobreescribir
    def eventos(self, lista_eventos):
        for evento in lista_eventos:
            if evento.type == KEYDOWN: 
                #Aceptar acción
                if evento.key == K_RETURN: 
                    elemento = self.elementosGUI.pop()
                    elemento.accion()
                    self.elementosGUI.append(elemento)
                          
                #Cambiar de opción
                if evento.key == K_DOWN or evento.key == K_UP:
                    if self.eventoSeleccionado == "continuar":
                        self.elementosGUI.pop()
                        self.addBotonSalir()
                    elif self.eventoSeleccionado == "salir":
                        self.elementosGUI.pop()
                        self.addBotonContinuar() 
                        
                if evento.type == pygame.QUIT: 
                    self.director.salirPrograma()                     


class TextoSalir(TextoGUI):
    def __init__(self, pantalla):
        # La fuente la debería cargar el estor de recursos
        fuente = pygame.font.SysFont('impact', 30);
        TextoGUI.__init__(self, pantalla, fuente, BLANCO, 'Salir', (65, 445))


class BotonSalir(Boton):
    def __init__(self, pantalla):
        Boton.__init__(self, pantalla, 'Menu/BotonGranada.png', (20,450))

    def accion(self):
        self.pantalla.menu.salirPrograma()

class TextoContinuar(TextoGUI):
    def __init__(self, pantalla):
        # La fuente la debería cargar el estor de recursos
        fuente = pygame.font.SysFont('impact', 30);
        TextoGUI.__init__(self, pantalla, fuente, BLANCO, 'Continuar', (65, 500))


class BotonContinuar(Boton):
    def __init__(self, pantalla):
        Boton.__init__(self, pantalla, 'Menu/BotonGranada.png', (20,500))

    def accion(self):
        self.pantalla.menu.crearCutScene()

