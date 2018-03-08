# -*- encoding: utf-8 -*-
import pygame
#import pyganim (?)
from pygame.locals import *
from gestorRecursos import *
from escena import *
from director import *
from fase import *
from PantallaConfiguracion import *
from pantallaInicial import *
from PantallaGameOver import *
from MenuGameOver import *

ANCHO_PANTALLA = 800
ALTO_PANTALLA =  600

# Clase Menu, la escena en sí
class Menu(Escena):
	def __init__(self, director):
		# Llamamos al constructor de la clase padre
		Escena.__init__(self, director);
		# Creamos la lista de pantallas
		self.listaPantallas = []
		# Creamos las pantallas que vamos a tener
		#   y las metemos en la lista
		self.listaPantallas.append(PantallaInicialGUI(self))
		self.listaPantallas.append(PantallaConfiguracionGUI(self,director))
		
		self.agregarAlDirectorEscenaGameOver()
		
		# En que pantalla estamos actualmente
		self.mostrarPantallaInicial()
		
	# Como el Menu de Game Over también va a volver hasta aquí también lo necesita.
	def agregarAlDirectorEscenaGameOver(self):
		escenaGameOver = MenuGameOver(self.director)
		self.director.agregarEscenaGameOver(escenaGameOver)
		
	def update(self, *args):
		return
    
	def eventos(self, lista_eventos):
	    # Se mira si se quiere salir de esta escena
		for evento in lista_eventos:
		    # Si se quiere salir, se le indica al director
			if evento.type == KEYDOWN:
				if evento.key == K_ESCAPE: #Salir
					self.salirPrograma()
				elif evento.key == K_g:
					self.mostrarPantallaGameOver()
					self.director.salirEscena()
			elif evento.type == pygame.QUIT: #Salir
				self.director.salirPrograma()

	
		# Se pasa la lista de eventos a la pantalla actual
		self.listaPantallas[self.pantallaActual].eventos(lista_eventos)
	
	def dibujar(self, pantalla):
		self.listaPantallas[self.pantallaActual].dibujar(pantalla)
    
	#--------------------------------------
	# Metodos propios del menu
    
	def salirPrograma(self):
		self.director.salirPrograma()
    
	def ejecutarJuego(self):
		self.mostrarPantallaConfiguracion() #Dejamos que esta sea la actual (si salimos de las fases entramos en esta)
		#fase2 = Fase(self.director,2)
		faseInicial = Fase(self.director,1)
		#self.director.apilarEscena(fase2)
		self.director.apilarEscena(faseInicial)
	
	def reanudarJuego(self,fase):
		self.director.apilarEscena(fase)
    
	def mostrarPantallaInicial(self):
		self.pantallaActual = 0
    
	def mostrarPantallaConfiguracion(self):
		self.pantallaActual = 1
	