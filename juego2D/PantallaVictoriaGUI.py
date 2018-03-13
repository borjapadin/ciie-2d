# -*- encoding: utf-8 -*-
import pygame
from pygame.locals import *
from gestorRecursos import *
from escena import *
from director import *
from fase import *
from PantallaGUI import *
from TextoGUI import *
from Boton import *

class PantallaVictoriaGUI(PantallaGUI):
	def __init__(self,menu):
		PantallaGUI.__init__(self,menu,'Victoria/decorado.png')
		
		#Creamos los botones y los metemos en la lista
		self.botonJugar = BotonVolverJugar(self)
		self.botonSalir = BotonSalir(self)
		
		self.elementosGUI.append(self,botonJugar)
		self.eventoSeleccionado = "jugar"
		
	def addBotonJugar(self):
		self.elementosGUI.pop()
		self.elementosGUI.append(self.botonJugar)
		self.eventoSeleccionado = "jugar"
		
	def addBotonSalir(self):
		self.elementosGUI.pop()
		self.elementosGUI.append(self.botonSalir)
		self.eventoSeleccionnado = "salir"
		
	def eliminarUltimosDosElementos(self):
		self.elementosGUI.pop()
		self.elementosGUI.pop()
		
	#Sobreescribir
	def eventos(self, lista_eventos):
		for evento in lista_eventos:
			if evento.type == KEYDOWN:
				#Aceptar accion
				if evento.key == K_RETURN:
					elemento = self.elementosGUI.pop()
					elemento.accion()
					
				#Cambiar la opción
				if evento.key == K_DOWN or evento.key == K_UP:
					if self.eventoSeleccionado == "jugar":
						self.addBotonSalir()
					elif self.eventoSeleccionado == "salir":
						self.addBotonJugar()
						
				if evento.type == pygame.QUIT:
					self.director.salirPrograma()
					
class TextoJugar(TextoGUI):
	def __init__(self, pantalla):
		fuente = pygame.font.SysFont('impact',30);
		TextoGUI.__init__(self, pantalla, fuente,(255,255,255), 'Empezar partida', (65,395))
		
	def accion(self):
		self.pantalla.menu.ejecutarJuego()
		
class TextoSalir(TextoGUI):
	def __init__(self, pantalla):
		fuente = pygame.font.SysFont('impact',30);
		TextoGUI.__init__(self, pantalla, fuente,(255,255,255), 'Salir partida', (65,445))
		
	def accion(self):
		self.menu.salirPrograma()
		
class BotonVolverJugar(Boton):
	def __init__(self,pantalla):
		Boton.__init__(self, pantalla, 'Victoria/BotonGranada.png', (20,400))
		
		def accion(self):
			self.pantalla.menu.ejecutarJuego()
			
class BotonSalir(Boton):
	def __init__(self,pantalla):
		Boton.__init__(self, pantalla, 'Victoria/BotonGranada.png',(20,445))
		
	def accion(self):
		self.pantalla.menu.salirPrograma()
		
