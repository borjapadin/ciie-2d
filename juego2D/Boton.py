# -*- encoding: utf-8 -*-
import pygame
#import pyganim (?)
from pygame.locals import *
from gestorRecursos import *
from escena import *
from director import *
from elementoGUI import *

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



################################################################################################


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


class BotonVolverJuego(Boton):
    def __init__(self, pantalla):
        Boton.__init__(self, pantalla, 'Menu/BotonGranada.png', (20,500))

    def accion(self):
        self.pantalla.menu.mostrarPantallaInicial()


class BotonReanudar(Boton):
    def __init__(self, pantalla, director):
        Boton.__init__(self, pantalla, 'Menu/BotonGranada.png', (20,400))
        self.director = director
        
    def accion(self):
        self.pantalla.menu.reanudarJuego(self.director.devolverEscenaPausada())


class BotonContinuar(Boton):
     def __init__(self, pantalla):
         Boton.__init__(self, pantalla, 'Menu/BotonGranada.png', (20,500))

     def accion(self):
        self.pantalla.menu.crearCutScene()
