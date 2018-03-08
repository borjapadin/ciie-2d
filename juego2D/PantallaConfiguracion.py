# -*- encoding: utf-8 -*-
import pygame
#import pyganim (?)
from pygame.locals import *
from gestorRecursos import *
from escena import *
from director import *
from fase import *
from menu import *
from PantallaGUI import *
from Boton import *

class PantallaConfiguracionGUI(PantallaGUI):
    def __init__(self,menu):
        PantallaGUI.__init__(self, menu, 'Menu/PantallaInicio.jpg')
        #botonReanudar = BotonReanudar(self,fase)
        #self.elementosGUI.append(botonReanudar)          
      #  textoJugar = TextoJugar(self)
        
        
    def asociarFaseActual(self,fase): 
        self.fase = fase
        #No puedo anadir el boton sin saber a que fase debe transicionar
        botonReanudar = BotonReanudar(self,fase)
        self.elementosGUI.append(botonReanudar)        
    
class BotonReanudar(Boton):
    def __init__(self, pantalla, fase):
        Boton.__init__(self, pantalla, 'Menu/BotonGranada.png', (20,400))
        self.fase = fase
        
    def accion(self):
        self.pantalla.menu.reanudarJuego(self.fase)