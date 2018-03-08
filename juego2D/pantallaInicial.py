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

        # Creamos el texto y lo metemos en la lista
        textoJugar = TextoJugar(self)
        textoSalir = TextoSalir(self)
        self.elementosGUI.append(textoJugar)
        self.elementosGUI.append(textoSalir)
       
        
        # Creamos los botones y los metemos en la lista
        self.botonJugar = BotonJugar(self)
        self.botonSalir = BotonSalir(self)
    
        self.elementosGUI.append(self.botonJugar)
        self.eventoSeleccionado = "jugar"
        #  self.elementosGUI.append(botonSalir)
        

    #Sobreescribir
    def eventos(self, lista_eventos):
        for evento in lista_eventos:
            
            if evento.type == MOUSEBUTTONDOWN: 
                self.elementoClic = None
                for elemento in self.elementosGUI: #Recorrer los elementos
                    if elemento.posicionEnElemento(evento.pos): #Ver si estan pulsados
                        self.elementoClic = elemento #Si esta encima el cursor estan clickados... 
                        #if isinstance(self.elementoClic, BotonAccion):
                        
            if evento.type == MOUSEBUTTONUP:
                for elemento in self.elementosGUI:
                    if elemento.posicionEnElemento(evento.pos):
                        if(elemento == self.elementoClic) :
                            elemento.accion()   
                            
            if evento.type == KEYDOWN: 
                #Aceptar acción
                if evento.key == K_RETURN: 
                    elemento = self.elementosGUI.pop()
                    elemento.accion()
                #    if self.eventoSeleccionado == "jugar":
                #        self.pantalla.menu.ejecutarJuego()                      
                #    elif self.eventoSeleccionado == "salir":
                #        self.director.salirPrograma()
                          
                #Cambiar de opción
                if evento.key == K_DOWN or evento.key == K_UP:
                    if self.eventoSeleccionado == "jugar":
                        self.elementosGUI.pop()
                        self.elementosGUI.append(self.botonSalir)
                        self.eventoSeleccionado = "salir"
                    elif self.eventoSeleccionado == "salir":
                        self.elementosGUI.pop()
                        self.elementosGUI.append(self.botonJugar)
                        self.eventoSeleccionado = "jugar"
                
                       
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

class BotonSalirNada(Boton):
    def __init__(self, pantalla):
        Boton.__init__(self, pantalla, 'Menu/BotonNada.png', (20,450))

class BotonEntrarNada(Boton):
    def __init__(self, pantalla):
        Boton.__init__(self, pantalla, 'Menu/BotonNada.png', (20,450))
