# -*- encoding: utf-8 -*-
import pygame
#import pyganim (?)
from pygame.locals import *
from gestorRecursos import *
from escena import *
from director import *
from fase import *
from pantallaConfiguracion import *
from pantallaInicial import *
from pantallaGameOver import *
from time import *
from Constantes import *
from pantallaVictoria import *
from pantallaCutScene import *

ANCHO_PANTALLA = 800
ALTO_PANTALLA =  600


# Clase Menu, la escena en sí
class Menu(Escena):
	def __init__(self, director):
		# Llamamos al constructor de la clase padre
		Escena.__init__(self, director);
		# Creamos la lista de pantallas
		self.listaPantallas = []

		######self.song = gestorRecursos.CargarSonido('');

		# Creamos las pantallas que vamos a tener
		#   y las metemos en la lista
		self.listaPantallas.append(PantallaInicialGUI(self))
		self.listaPantallas.append(PantallaConfiguracionGUI(self,director))
		self.listaPantallas.append(PantallaGameOverGUI(self))
		self.listaPantallas.append(PantallaVictoriaGUI(self))
		self.listaPantallas.append(PantallaCutSceneGUI(self))
		
		# En que pantalla estamos actualmente
		#self.mostrarPantallaInicial()
		self.mostrarPantalla(PANTALLA_PRINCIPAL)
		
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
    
	#--------------------------------------
	# Metodos propios del menu
    
	def salirPrograma(self):
		self.director.salirPrograma()
    
	def ejecutarJuego(self):
		self.crearCutScene()
		#fase2 = Fase(self.director,2)
	#	cutscene = CutScene(self.director,NUM_FASE_INICIAL)
	#	self.director.apilarEscena(cutscene)
	#	self.mostrarPantallaConfiguracion() 
	
	def crearCutScene(self):
		#El menú ya sabe cual es la fase siguiente.
		cutscene = CutScene(self.director,self.numFaseSiguiente)
		#Puede saberlo porque se ha inicializado con que es la fase inicial o por la información
		#Que proporciona el director obteniendola de la fase terminada 
		self.director.apilarEscena(cutscene)
		#self.mostrarPantallaConfiguracion() #Dejamos que esta sea la actual (si salimos de las fases entramos en esta)
		self.mostrarPantalla(PANTALLA_PAUSA)
	def reanudarJuego(self,fase):
		self.director.apilarEscena(fase)
	
	def setNumFaseSiguiente(self,numFaseSiguiente):
		self.numFaseSiguiente = numFaseSiguiente
	



################################################################################	

	def mostrarPantalla(self, pantalla):
			self.pantallaActual = pantalla 


	"""def mostrarPantallaInicial(self):
		self.pantallaActual = PANTALLA_PRINCIPAL
    
	def mostrarPantallaConfiguracion(self):
		self.pantallaActual = PANTALLA_PAUSA

	def mostrarPantallaGameOver(self):
		self.pantallaActual = PANTALLA_GAMEOVER
	
	def mostrarPantallaVictoria(self):
		self.pantallaActual = PANTALLA_VICTORIA
	
	def mostrarPantallaCutScene(self):
		self.pantallaActual = PANTALLA_CUTSCENE """
	
