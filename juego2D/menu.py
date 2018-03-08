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
		self.listaPantallas.append(PantallaConfiguracionGUI(self))
		# En que pantalla estamos actualmente
		self.mostrarPantallaInicial()
    
	def update(self, *args):
		return
    
	def eventos(self, lista_eventos):
	    # Se mira si se quiere salir de esta escena
		for evento in lista_eventos:
		    # Si se quiere salir, se le indica al director
			if evento.type == KEYDOWN:
				if evento.key == K_ESCAPE: #Salir
					self.salirPrograma()
				#elif evento.key == K_p: #Aquí deberia hacer un menu de pausa que aparezca****
					#print("Menu de pausa")
				#	self.mostrarPantallaConfiguracion()	
					#self.apilarEscena(
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
		fase = Fase(self.director,"/1-Bosque")
		self.mostrarPantallaConfiguracion(fase) #Dejamos que esta sea la actual (si salimos de las fases entramos en esta)
		#fase2Playa = Fase(self.director,"/2-Playa")
		#fase3Bunker = Fase(self.director,"3-Bunker")
		#self.director.apilarEscena(fase2Playa)
		self.director.apilarEscena(fase)
	
	def reanudarJuego(self,fase):
		self.director.apilarEscena(fase)
    
	def mostrarPantallaInicial(self):
		self.pantallaActual = 0
    
	def mostrarPantallaConfiguracion(self,fase):
		self.pantallaActual = 1
		self.listaPantallas[self.pantallaActual].asociarFaseActual(fase)
	
	def mostrarPantallaGameOver(self):
		self.pantallaActual = 2
	
	def mostrarPantallaBomb(self):
		self.pantallaActual = 3
