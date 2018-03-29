# -*- encoding: utf-8 -*-
import pygame
#import pyganim (?)
from pygame.locals import *
from gestorRecursos import *
from escena import *
from director import *
from fase import *
from time import *
from constantes import *
from pantalla import *
from cutscene import *

ANCHO_PANTALLA = 800
ALTO_PANTALLA =  600


# Clase Menu, la escena en sí
class Menu(Escena):
	def __init__(self, director):
		Escena.__init__(self, director); # Llamamos al constructor de la clase padre

		self.listaPantallas = [] # Creamos la lista de pantallas

		# Creamos las pantallas que vamos a tener y las metemos en la lista
		self.listaPantallas.append(Pantalla(self, director, 'Menu/Inicio/PantallaInicio.jpg'))
		self.listaPantallas.append(Pantalla(self, director, 'Menu/Pausa/PantallaPausa.png'))
		self.listaPantallas.append(Pantalla(self, director, 'Menu/GameOver/PantallaGameOver_2.jpg'))
		self.listaPantallas.append(Pantalla(self, director, 'Menu/Victoria/PantallaVictoria.png'))
		self.listaPantallas.append(Pantalla(self, director, 'Menu/CutScene/PantallaSiguienteNivel.png'))

		
		# En que pantalla estamos actualmente
		self.mostrarPantalla(PANTALLA_PRINCIPAL)
		self.vida = 1000
		#Para saber cual es la primera fase que creara cutScene.
		#Con el número (de la fase y cutscene) gestionamos el comportamiento que debe tener esa fase como:
		#Que imagen cargar de donde en cutScene, que texto, cual seria la fase siguiente etc.
		self.setNumFaseSiguiente(NUM_FASE_INICIAL)
	
	def update(self, *args):
		return
    
	def eventos(self, lista_eventos):
	    # Se mira si se quiere salir de esta escena
		for evento in lista_eventos:
		    # Si se quiere salir, se le indica al director
			if evento.type == KEYDOWN:
				if evento.key == K_ESCAPE: #Salir
					self.salirPrograma()
			elif evento.type == pygame.QUIT: #Salir
				self.director.salirPrograma()

	
		# Se pasa la lista de eventos a la pantalla actual
		self.listaPantallas[self.pantallaActual].eventos(lista_eventos)
	
	def dibujar(self, pantalla):
		self.listaPantallas[self.pantallaActual].dibujar(pantalla)
    

	# Metodos propios del menu 
	def salirPrograma(self):
		self.director.salirPrograma()
    
	def ejecutarJuego(self):
		self.crearCutScene()
	
	def crearCutScene(self):
		#El menú ya sabe cual es la fase siguiente.
		cutscene = CutScene(self.director,self.numFaseSiguiente)
		#Puede saberlo porque se ha inicializado con que es la fase inicial o por la información
		#Que proporciona el director obteniendola de la fase terminada 
		self.director.apilarEscena(cutscene)

	def reanudarJuego(self,fase):
		self.director.apilarEscena(fase)
	
	def setNumFaseSiguiente(self,numFaseSiguiente):
		self.numFaseSiguiente = numFaseSiguiente
		
	def mostrarPantalla(self, pantalla):
		self.pantallaActual = pantalla