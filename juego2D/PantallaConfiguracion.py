# -*- encoding: utf-8 -*-
import pygame
#import pyganim (?)
from pygame.locals import *
from gestorRecursos import *
from escena import *
from director import *
from fase import *
from menu import *
from pantallaGUI import *
from boton import *

class PantallaConfiguracionGUI(PantallaGUI):
    def __init__(self,menu,director):
        PantallaGUI.__init__(self, menu, 'Menu/Pausa/PantallaPausa.png')
        self.director = director #Para que indique en que fase esta
        
        botonReanudar = BotonReanudar(self,director)
        self.elementosGUI.append(botonReanudar)        
        

#################################################################    
# class BotonReanudar(boton):
    # def __init__(self, pantalla, director):
    #     boton.__init__(self, pantalla, 'Menu/BotonGranada.png', (20,400))
    #     self.director = director
        
    # def accion(self):
    #     self.pantalla.menu.reanudarJuego(self.director.devolverEscenaPausada()) 
#################################################################   

