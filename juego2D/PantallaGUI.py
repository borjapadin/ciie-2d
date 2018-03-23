# -*- encoding: utf-8 -*-
import pygame
#import pyganim (?)
from pygame.locals import *
from gestorRecursos import *
from escena import *
from director import *
from fase import *
from menu import *
from boton import *
#from PantallaConfiguracion import *
#from PantallaInicial import *

#Clase PantallaGUI y las distintas pantallas
class PantallaGUI:
    def __init__(self, menu, nombreImagen):
        self.menu = menu
        #Se carga la imagen de fondo
        self.imagen = GestorRecursos.CargarImagen(nombreImagen,1)
        self.imagen = pygame.transform.scale(self.imagen, (ANCHO_PANTALLA, ALTO_PANTALLA))
        #Se tiene una lista de elementos GUI
        self.elementosGUI = []
        #Se tiene una lista de animaciones
       # self.animaciones = []

    def eventos(self, lista_eventos): #Actualmente no usa esto ninguna porque hay una clase que la sobreescribe, pero dejemoslo de momento
        for evento in lista_eventos:
            if evento.type == MOUSEBUTTONDOWN: 
                self.elementoClic = None
                for elemento in self.elementosGUI:
                    if elemento.posicionEnElemento(evento.pos):
                        self.elementoClic = elemento
            if evento.type == MOUSEBUTTONUP:
                for elemento in self.elementosGUI:
                    if elemento.posicionEnElemento(evento.pos):
                        if(elemento == self.elementoClic) :
                            elemento.accion()
                
                
    def dibujar(self, pantalla):
        #Dibujamos primero la imagen de fondo
        pantalla.blit(self.imagen, self.imagen.get_rect())
        #Después las animaciones
    #	for animacion in self.animaciones:
    #		animacion.dibujar(pantalla)
        #Después los botones
        for elemento in self.elementosGUI:
            elemento.dibujar(pantalla)



class PantallaConfiguracionGUI(PantallaGUI):
    def __init__(self,menu,director):
        PantallaGUI.__init__(self, menu, 'Menu/Pausa/PantallaPausa.png')
        self.director = director #Para que indique en que fase esta
        
        botonReanudar = BotonReanudar(self,director)
        self.elementosGUI.append(botonReanudar)     
# -----------