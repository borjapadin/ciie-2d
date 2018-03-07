# -*- encoding: utf-8 -*-
import pygame
#import pyganim (?)
from pygame.locals import *
from gestorRecursos import *
from escena import *
from director import *
from fase import *

ANCHO_PANTALLA = 800
ALTO_PANTALLA =  600

#Clase abstracta ElementoGUI
class ElementoGUI:
	def __init__(self, pantalla, rectangulo):
		self.pantalla = pantalla
		self.rect = rectangulo

	#Método para situarlo en la pantalla
	def establecerPosicion(self, posicion):
		(posicionx, posiciony) = posicion
		self.rect.left = posicionx
		self.rect.bottom = posiciony

	#Te dice si se ha hecho clic en el
	def posicionEnElemento(self, posicion):
		(posicionx, posiciony) = posicion
		if (posicionx>=self.rect.left) and (posicionx<=self.rect.right) and (posiciony>=self.rect.top) and (posiciony<=self.rect.bottom):
			return True
		else:
			return False

	#Métodos abstractos
	def dibujar(self):
		raise NotImplemented("Tiene que implementar el metodo dibujar")

	def accion(self):
		raise NotImplemented("Tiene que implementar el metodo de accion")

#Clase Boton con los correspondientes botones
class Boton(ElementoGUI):
	def __init__(self, pantalla, nombreImagen, posicion):
		#Se carga la imagen del boton
		self.imagen = GestorRecursos.CargarImagen(nombreImagen,-1)
		self.imagen = pygame.transform.scale(self.imagen,(45,45))
		#Se llama al ´método de la clase padre con el rectángulo que ocupa el botón
		ElementoGUI.__init__(self, pantalla, self.imagen.get_rect())
		#Se coloca el rectángulo en su posición
		self.establecerPosicion(posicion)

	def dibujar(self,pantalla):
		pantalla.blit(self.imagen,self.rect)

class BotonJugar(Boton):
	def __init__(self, pantalla):
		Boton.__init__(self, pantalla, 'Menu/BotonGranada.png', (20,400))

	def accion(self):
		self.pantalla.menu.ejecutarJuego()

class BotonSalir(Boton):
	def __init__(self, pantalla):
		Boton.__init__(self, pantalla, 'Menu/BotonGranada.png', (20,450))

	def accion(self):
		self.pantalla.menu.salirPrograma()

#Clase TextoGUI y los distintos textos

class  TextoGUI(ElementoGUI):
	def __init__(self, pantalla, fuente, color, texto, posicion):
		#Se crea la imagen del texto
		self.imagen = fuente. render(texto, True, color)
		#Se llama al método de la clase padre con el rectángulo que ocupa el texto
		ElementoGUI.__init__(self, pantalla, self.imagen.get_rect())
		#Se coloca el rectangulo en su posicion
		self.establecerPosicion(posicion)

	def dibujar(self, pantalla):
		pantalla.blit(self.imagen, self.rect)

class TextoJugar(TextoGUI):
	def __init__(self, pantalla):
		# La fuente la debería cargar el estor de recursos
		fuente = pygame.font.SysFont('impact', 30);
		TextoGUI.__init__(self, pantalla, fuente, (255, 255, 255), 'Empezar partida', (60, 395))
	def accion(self):
		self.pantalla.menu.ejecutarJuego()

class TextoSalir(TextoGUI):
	def __init__(self, pantalla):
		# La fuente la debería cargar el estor de recursos
		fuente = pygame.font.SysFont('impact', 30);
		TextoGUI.__init__(self, pantalla, fuente, (255, 255, 255), 'Salir', (60, 445))
	def accion(self):
		self.pantalla.menu.salirPrograma()

#Clase PantallaGUI y las distintas pantallas
class PantallaGUI:
	def __init__(self, menu, nombreImagen):
		self.menu = menu
		#Se carga la imagen de fondo
		self.imagen = GestorRecursos.CargarImagen(nombreImagen,1)
		self.imagen = pygame.transform.scale(self.imagen, (ANCHO_PANTALLA, ALTO_PANTALLA))
		#Se tiene una lista de elementos GUI
		self.elementosGUI = []
		#Se tiene una lista de animaciones
		self.animaciones = []

	def eventos(self, lista_eventos):
		for evento in lista_eventos:
			if evento.type == MOUSEBUTTONDOWN:
				self.elementoClic = None
				for elemento in self.elementosGUI:
					if elemento.posicionEnElemento(evento.pos):
						self.elementoClic = elemento
			if evento.type == MOUSEBUTTONUP:
				for elemento in self.elementosGUI:
					if elemento.posicionEnElemento(evento.pos):
						if(elemento == self.elementoClic):
							elemento.accion()
	

	def dibujar(self, pantalla):
		#Dibujamos primero la imagen de fondo
		pantalla.blit(self.imagen, self.imagen.get_rect())
		#Después las animaciones
	#	for animacion in self.animaciones:
	#		animacion.dibujar(pantalla)
		#Después los botones
		for elemento in self.elementosGUI:
			elemento.dibujar(pantalla)
			
class PantallaInicialGUI(PantallaGUI):
	def __init__(self, menu):
		PantallaGUI.__init__(self, menu, 'Menu/PantallaInicio.jpg')

		# Creamos los botones y los metemos en la lista
		botonJugar = BotonJugar(self)
		botonSalir = BotonSalir(self)
		
		self.elementosGUI.append(botonJugar)
		self.elementosGUI.append(botonSalir)
		
		# Creamos el texto y lo metemos en la lista
		textoJugar = TextoJugar(self)
		textoSalir = TextoSalir(self)
		self.elementosGUI.append(textoJugar)
		self.elementosGUI.append(textoSalir)

class PantallaConfiguracionGUI(PantallaGUI):
	def __init__(self,menu):
		PantallaGUI.__init__(self, menu, 'Menu/PantallaInicio.jpg')
	
# -------------------------------------------------
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
				elif evento.key == K_p: #Aquí deberia hacer un menu de pausa que aparezca****
					#print("Menu de pausa")
					#self.mostrarPantallaConfiguracion()	
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
		fase1Bosque = Fase(self.director,"/1-Bosque")
		fase2Playa = Fase(self.director,"/2-Playa")
		#fase3Bunker = Fase(self.director,"3-Bunker")
		self.director.apilarEscena(fase2Playa)
		self.director.apilarEscena(fase1Bosque)
    
	def mostrarPantallaInicial(self):
		self.pantallaActual = 0
    
	def mostrarPantallaConfiguracion(self):
		self.pantallaActual = 1
	
	def mostrarPantallaGameOver(self):
		self.pantallaActual = 2
	
	def mostrarPantallaBomb(self):
		self.pantallaActual = 3
