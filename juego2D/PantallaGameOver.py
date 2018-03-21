# -*- encoding: utf-8 -*-
import pygame
#import pyganim (?)
from pygame.locals import *
from gestorRecursos import *
from escena import *
from director import *
from fase import *
from pantallaGUI import *
from textoGUI import *
from boton import *
from Constantes import *

class PantallaGameOverGUI(PantallaGUI):
    def __init__(self, menu):
        PantallaGUI.__init__(self, menu, 'Menu/GameOver/PantallaGameOver_2.jpg')
        
        # Creamos el texto y lo metemos en la lista
        textoSalir = TextoSalir(self)
        self.elementosGUI.append(textoSalir) 
        textoVolverJuego = TextoVolverJuego(self)
        self.elementosGUI.append(textoVolverJuego)
        
        #Creamos los botones
        self.botonSalir = BotonSalir(self)      
        self.botonVolverJuego = BotonVolverJuego(self)
        #Agregamos solo el que va a estar seleccionado la primera vez que se cree
        self.addBotonJugar()
    
    def addBotonJugar(self):
        self.elementosGUI.append(self.botonVolverJuego)
        self.eventoSeleccionado = "volverJugar"        
        
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
                    if self.eventoSeleccionado == "volverJugar":
                        self.elementosGUI.pop()
                        self.addBotonSalir()
                    elif self.eventoSeleccionado == "salir":
                        self.elementosGUI.pop()
                        self.addBotonJugar() 
                        
                if evento.type == pygame.QUIT: #EHHHHHHHHHHHHHHHHH... si?
                    self.director.salirPrograma()                     


# class TextoSalir(textoGUI):
#     def __init__(self, pantalla):
#         # La fuente la debería cargar el estor de recursos
#         fuente = pygame.font.SysFont('impact', 30);
#         textoGUI.__init__(self, pantalla, fuente, BLANCO, 'Salir', (65, 445))

# class TextoVolverJuego(textoGUI):
#     def __init__(self, pantalla):
#         # La fuente la debería cargar el estor de recursos
#         fuente = pygame.font.SysFont('impact', 30);
#         textoGUI.__init__(self, pantalla, fuente, BLANCO, 'Volver a jugar', (65, 500))



############################################################################################3
# class BotonSalir(boton):
#     def __init__(self, pantalla):
#         boton.__init__(self, pantalla, 'Menu/BotonGranada.png', (20,450))

#     def accion(self):
#         self.pantalla.menu.salirPrograma()

# class BotonVolverJuego(boton):
#     def __init__(self, pantalla):
#         boton.__init__(self, pantalla, 'Menu/BotonGranada.png', (20,500))

#     def accion(self):
#         self.pantalla.menu.mostrarPantallaInicial()
############################################################################################
