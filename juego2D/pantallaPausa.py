# -*- encoding: utf-8 -*-
import pygame
#import pyganim (?)     
from pygame.locals import *
from gestorRecursos import *
from director import *
from escena import *
from fase import *
from pantallaGUI import *
from textoGUI import *
from boton import *
from constantes import *

class PantallaPausa(PantallaGUI):
	def __init__(self,menu,director):
		PantallaGUI.__init__(self, menu, 'Menu/Pausa/PantallaPausa.png')
 	      	self.director = director #Para que indique en que fase esta
 	       
		textoContinuar = TextoContinuar(self) 
		self.elementosGUI.append(textoContinuar)
	
 	       	self.botonReanudar = BotonReanudar(self,director)
 	       	self.elementosGUI.append(self.botonReanudar) 

		self.addBotonReanudar()

	def addBotonReanudar(self):
        	self.elementosGUI.append(self.botonReanudar)
        	self.eventoSeleccionado = "volverJugar"

	        
	def addBotonSalir(self):
        	self.elementosGUI.append(self.botonSalir)
        	self.eventoSeleccionado = "salir" 

	def eventos(self, lista_eventos):
        	for evento in lista_eventos:
            		if evento.type == KEYDOWN: 
                		#Aceptar acción
                		if evento.key == K_RETURN: 
                    			elemento = self.elementosGUI.pop()
                    			elemento.accion()
                    			self.elementosGUI.append(elemento)  
  
                	
                        
    


