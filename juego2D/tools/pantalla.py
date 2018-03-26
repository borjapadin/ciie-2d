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

        if self.imagen == 'Menu/CutScene/PantallaSiguienteNivel.png':
            textoSalir = TextoSalir(self)
            textoContinuar = TextoContinuar(self)

            self.elementosGUI.append(textoSalir) 
            self.elementosGUI.append(textoContinuar)

            self.botonSalir = BotonSalir(self)   
            self.botonContinuar = BotonContinuar(self)

            self.addBotonContinuar()
     
        elif self.imagen == 'Menu/Inicio/PantallaInicio.jpg':
            textoJugar = TextoJugar(self)
            textoSalir = TextoSalir(self)

            self.elementosGUI.append(textoJugar) 
            self.elementosGUI.append(textoSalir) 

            self.botonJugar = BotonJugar(self)
            self.botonSalir = BotonSalir(self)

            self.addBotonJugar()
            
        elif self.imagen == 'Menu/GameOver/PantallaGameOver_2.jpg' and self.imagen == 'Menu/Victoria/PantallaVictoria.png':
            textoSalir = TextoSalir(self)
            self.elementosGUI.append(textoSalir) 
            textoVolverJuego = TextoVolverJuego(self)
            self.elementosGUI.append(textoVolverJuego)
        
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
                    elif self.eventoSeleccionado == "salir" and self.imagen == 'Menu/CutScene/PantallaSiguienteNivel.png':
                        self.elementosGUI.pop()
                        self.addBotonContinuar()                        
                    elif self.eventoSeleccionado == "continuar":
                        self.elementosGUI.pop()
                        self.addBotonSalir()
                    elif self.eventoSeleccionado == "jugar":
                        self.elementosGUI.pop()
                        self.addBotonSalir()
                    elif self.eventoSeleccionado == "salir" and self.imagen == 'Menu/GameOver/PantallaGameOver_2.jpg' and self.imagen == 'Menu/Victoria/PantallaVictoria.png' :
                        self.elementosGUI.pop()
                        self.addBotonVolverJugar()
                        
                if evento.type == pygame.QUIT: 
                    self.director.salirPrograma()                     
