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
    def __init__(self, menu, imagen):
        PantallaGUI.__init__(self, menu, imagen)
        
         # Creamos el texto y lo metemos en la lista
        textoSalir = TextoSalir(self)
        self.elementosGUI.append(textoSalir) 
        self.botonSalir = BotonSalir(self)   

        if imagen == 'Menu/CutScene/PantallaSiguienteNivel.png':
            textoContinuar = TextoContinuar(self)
            self.elementosGUI.append(textoContinuar)
            self.botonContinuar = BotonContinuar(self)
            self.addBotonContinuar()
     
        elif imagen == 'Menu/Inicio/PantallaInicio.jpg':
            textoJugar = TextoJugar(self)
            self.elementosGUI.append(textoJugar) 
            self.botonJugar = BotonJugar(self)
            self.addBotonJugar()
        else:
            textoVolverJuego = TextoVolverJuego(self)
            self.elementosGUI.append(textoVolverJuego)
            self.botonVolverJuego = BotonVolverJuego(self)
            self.addBotonVolverJuego()
    
    
    def addBotonContinuar(self):
        self.elementosGUI.append(self.botonContinuar)
        self.eventoSeleccionado = "continuar"        
        
    def addBotonSalir(self):
        self.elementosGUI.append(self.botonSalir)
        self.eventoSeleccionado = "salir"   

    
    def addBotonJugar(self):
        self.elementosGUI.append(self.botonJugar)
        self.eventoSeleccionado = "jugar"        
    
    def addBotonVolverJuego(self):
        self.elementosGUI.append(self.botonVolverJuego)
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
                    self.elementosGUI.pop()
                    if self.eventoSeleccionado == "jugar":
                        if imagen == 'Menu/CutScene/PantallaSiguienteNivel.png' or imagen == 'Menu/Inicio/PantallaInicio.jpg':
                        	self.addBotonContinuar() 
                    else:
                        self.addBotonSalir()
                        
                if evento.type == pygame.QUIT: 
                    self.director.salirPrograma()                     
