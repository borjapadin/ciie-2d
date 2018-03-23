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
from constantes import *

class PantallaVGO(PantallaGUI):
    def __init__(self, menu, imagen):
        PantallaGUI.__init__(self, menu, imagen)
        
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
