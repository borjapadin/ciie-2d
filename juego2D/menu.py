# -*- encoding: utf-8 -*-
import pygame
#import pyganim (?)
from pygame.locals import *
from gestorRecursos import *
from escena import *
from director import *

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
		if(posicionx >= self.rect.left) and (posicionx<=self.rect.rigth) and (posiciony>=self.rect.top) and (posiciony<=self.rect.bottom):
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
		self.imagen = pygame.transform.scale(self.imagen,(20,20))
		#Se llama al ´método de la clase padre con el rectángulo que ocupa el botón
		ElementoGUI.__init__(self, pantalla, self.imagen.get_rect())
		#Se coloca el rectángulo en su posición
		self.establecerPosicion(posicion)

	def dibujar(self,pantalla):
		pantalla.blit(self.imagen,self.rect)

class BotonJugar(Boton):
	def __init__(self, pantalla):
		Boton.__init__(self, pantalla, 'boton_verde.png', (580,530))

	def accion(self):
		self.pantalla.menu.ejecutarJuego()

class BotonSalir(Boton):
	def __init__(self, pantalla):
		Boton.__init__(self, pantalla, 'boton_rojo.png', (580,530))

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

#Clase PantallaGUI y las distintas pantallas

class PantallaGUI:
	def __init__(self, menu, nombreImagen):
		self.menu = menu
		#Se carga la imagen de fondo
		self.imagen = GestorRecursos.CargarImagen(nombreImagen)
		self.imagen = pygame.transform.scale(self.imagen, (ANCHO_PANTALLA, ALTO_PANTALLA))
		#Se tiene una lista de elementos GUI
		self.elementoGUI = []
		#Se tiene una lista de animaciones
		self.animaciones = []

	def eventos(self, lista_eventos):
		for evento in lista_eventos:
			if evento.type == MOUSEBUTTONDOWN:
				self.elementoClic = None
				for elemento in self.elementoGUI:
					if elemento.posicionEnElemento(evento.pos):
						self.elementoClic = elemento
			if elemento.type == MOUSEBUTTONUP:
				for elemento in self.elementoGUI:
					if elemento.posicionEnElemento(evento.pos):
						if(elemento == self.elementoClic):
							elemento.accion()

	def dibujar(self, pantalla):
		#Dibujamos primero la imagen de fondo
		pantalla.blit(self.imagen, self.imagen.get_rect())
		#Después las animaciones
		for animacion in self.animaciones:
			animacion.dibujar(pantalla)
		#Después los botones
		for elemento in self.elementoGUI:
			elemento.dibujar(pantalla)
			
class PantallaInicialGUI(PantallaGUI):
	def __init__(self, menu):
		PantallaGUI.__init__(self, menu, 'Menu\PantallaInicio.jpg')
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
		# En que pantalla estamos actualmente
		self.mostrarPantallaInicial()
    
	def update(self, *args):
		return
    
	def eventos(self, lista_eventos):
	    # Se mira si se quiere salir de esta escena
		for evento in lista_eventos:
		    # Si se quiere salir, se le indica al director
			if evento.type == KEYDOWN:
				if evento.key == K_ESCAPE:
					self.salirPrograma()
			elif evento.type == pygame.QUIT:
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
		fase = Fase(self.director)
		self.director.apilarEscena(fase)
    
	def mostrarPantallaInicial(self):
		self.pantallaActual = 0
    
	# def mostrarPantallaConfiguracion(self):
	#    self.pantallaActual = ...
