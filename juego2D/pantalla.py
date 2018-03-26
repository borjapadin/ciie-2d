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

class Pantalla(PantallaGUI):
	def __init__(self, menu, director, imagen):
	        PantallaGUI.__init__(self, menu, director, imagen)
        
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
	                self.botonSalirPantallaIni = BotonSalir(self)
    
	                self.addBotonJugar()
                    
	        elif imagen == 'Menu/Pausa/PantallaPausa.png':
                	self.director = director #Para que indique en que fase esta
           
                	textoContinuar = TextoContinuar(self) 
                	self.elementosGUI.append(textoContinuar)
    
                	self.botonReanudar = BotonReanudar(self,director)
                	self.elementosGUI.append(self.botonReanudar)    
	        else:
	                textoVolverJuego = TextoVolverJuego(self) 
	                textoSalir = TextoSalir(self)
    
	                self.elementosGUI.append(textoVolverJuego)
	                self.elementosGUI.append(textoSalir)
         
	                #Creamos los botones
	                self.botonSalir = BotonSalir(self) 
	                self.botonVolverJuego = BotonVolverJuego(self)
    
	                #Agregamos solo el que va a estar seleccionado la primera vez que se cree
	                self.addBotonVolverJugar()
    
    
    
	def addBotonContinuar(self):
	        self.elementosGUI.append(self.botonContinuar)
        	self.eventoSeleccionado = "continuar"            
        
    	def addBotonSalir(self):
        	self.elementosGUI.append(self.botonSalir)
        	self.eventoSeleccionado = "salir"   

    	def addBotonJugar(self):
       		self.elementosGUI.append(self.botonJugar)
        	self.eventoSeleccionado = "jugar"        
    
    	def addBotonVolverJugar(self):
        	self.elementosGUI.append(self.botonVolverJuego)
        	self.eventoSeleccionado = "volverJugar" 

    	def addBotonSalirCuteScene(self):
        	self.elementosGUI.append(self.botonCuteSceneSalir)
        	self.eventoSeleccionado = "salirCuteScene" 

        def addbBotonSalirPantallaIni(self):
            	self.elementosGUI.append(self.botonSalirPantallaIni)
            	self.eventoSeleccionado = "salirPantallaIni" 

       	def addBotonReanudar(self):
            	self.elementosGUI.append(self.botonReanudar)
            	self.eventoSeleccionado = "volverJugar"


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
                        
                    			elif self.eventoSeleccionado == "salirPantallaIni":  
                        			self.elementosGUI.pop()
                        			self.addBotonJugar()

                    			elif self.eventoSeleccionado == "jugar":
                        			self.elementosGUI.pop()
                        			self.addbBotonSalirPantallaIni()

                    			elif self.eventoSeleccionado == "salirCuteScene":
                        			self.elementosGUI.pop()
                        			self.addBotonContinuar() 

                    			elif self.eventoSeleccionado == "continuar":
                        			self.elementosGUI.pop()
                       				self.addBotonSalirCuteScene()

                                	else:
                                    		self.elementosGUI.pop()
                                    		self.addBotonVolverJugar()

                        
                		if evento.type == pygame.QUIT: 
                    			self.director.salirPrograma()                     
