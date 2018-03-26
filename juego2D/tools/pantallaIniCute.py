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

class PantallaIniCute(PantallaGUI):
	def __init__(self, menu, imagen):     
		PantallaGUI.__init__(self, menu, imagen)
        
	        if imagen == 'Menu/CutScene/PantallaSiguienteNivel.png':
               		textoContinuar = TextoContinuar(self)
                	self.elementosGUI.append(textoContinuar)
	            	textoSalir = TextoSalir(self)
	            	self.elementosGUI.append(textoSalir) 
	       	    
	            	self.botonContinuar = BotonContinuar(self)   
	            	self.botonCuteSceneSalir = BotonSalir(self)   
	                    
	            	self.addBotonContinuar()
     
	        elif imagen == 'Menu/Inicio/PantallaInicio.jpg':
	        	textoJugar = TextoJugar(self)
	            	textoSalir = TextoSalir(self)
	
	            	self.elementosGUI.append(textoJugar) 
	            	self.elementosGUI.append(textoSalir) 
	
	           	self.botonJugar = BotonJugar(self)
	            	self.botonSalir = BotonSalir(self)
	
	            	self.addBotonJugar()
	   

	def addBotonContinuar(self):
	        self.elementosGUI.append(self.botonContinuar)
	        self.eventoSeleccionado = "continuar"        
        
    
	def addBotonJugar(self):
	        self.elementosGUI.append(self.botonJugar)
	        self.eventoSeleccionado = "jugar"  
 
	def addBotonSalirCuteScene(self):
	        self.elementosGUI.append(self.botonCuteSceneSalir)
	        self.eventoSeleccionado = "salirCuteScene" 
	
	def addBotonSalir(self):
	        self.elementosGUI.append(self.botonSalir)
	        self.eventoSeleccionado = "salir"   

	"""def addBoton(self, evento, boton):
		self.elementosGUI.append(self.boton)
		self.eventoSeleccionado = evento """

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
                		        	self.addBotonSalirCuteScene()

		    			elif self.eventoSeleccionado == "jugar":
                        			self.elementosGUI.pop()
                        			self.addBotonSalir()
                    			elif self.eventoSeleccionado == "salirCuteScene":
                        			self.elementosGUI.pop()
                        			self.addBotonContinuar()
 
                    			else:
                        			self.elementosGUI.pop()
                        			self.addBotonJugar()     
                        
                		if evento.type == pygame.QUIT: 
                    			self.director.salirPrograma()                     
