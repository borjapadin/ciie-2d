# -*- encoding: utf-8 -*-

# Modulos
import pygame
import sys
#import escena
from escena import *
from pygame.locals import *
from Constantes import *

class Director():

    def __init__(self):
        # Inicializamos la pantalla y el modo grafico
        self.screen = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
        pygame.display.set_caption("Juego con escenas")
        # Pila de escenas
        self.pila = []
        # Flag que nos indica cuando quieren salir de la escena
        self.salir_escena = False
        # Reloj
        self.reloj = pygame.time.Clock()


    def bucle(self, escena):

        # Cogemos el reloj de pygame
        #reloj = pygame.time.Clock()

        self.salir_escena = False

        # Eliminamos todos los eventos producidos antes de entrar en el bucle
        pygame.event.clear()
        
        # El bucle del juego, las acciones que se realicen se harán en cada escena
        while not self.salir_escena:

            # Sincronizar el juego a 60 fps
            tiempo_pasado = self.reloj.tick(60)

            # Pasamos los eventos a la escena
            escena.eventos(pygame.event.get())

            # Actualiza la escena
            escena.update(tiempo_pasado)

            # Se dibuja en pantalla
            escena.dibujar(self.screen)
            pygame.display.flip()


    def ejecutar(self):

        # Mientras haya escenas en la pila, ejecutaremos la de arriba
        while (len(self.pila)>0):

            # Se coge la escena a ejecutar como la que este en la cima de la pila
            escena = self.pila[len(self.pila)-1]

            # Ejecutamos el bucle de eventos hasta que termine la escena
            self.bucle(escena)


    def salirEscena(self):
        # Indicamos en el flag que se quiere salir de la escena
        self.salir_escena = True
        # Eliminamos la escena actual de la pila (si la hay)
        if (len(self.pila)>0):
            self.pila.pop()

    def salirPrograma(self):
        # Vaciamos la lista de escenas pendientes
        self.pila = []
        self.salir_escena = True
        
    def cambiarAlMenu(self,fase,pantalla):
        self.escenaPausada(fase)
        self.salirEscena()
        
        #Modificar parámetro del menu.
        menu = self.pila.pop() #Saco el menu para cambiar el parámetro
        if (pantalla == PANTALLA_PAUSA): 
            menu.mostrarPantallaConfiguracion()
        elif (pantalla == PANTALLA_GAMEOVER):
            menu.mostrarPantallaGameOver()  
        elif (pantalla == PANTALLA_VICTORIA):
            menu.mostrarPantallaVictoria()
        elif (pantalla == PANTALLA_CUTSCENE):
            menu.mostrarPantallaCutScene()
            menu.setNumFaseSiguiente(fase.obtenerNumeroFaseSiguiente())#El director le da a menu el número de fase indicado por la fase 
            #Esto es así porque el número de fase es necesario para saber que cutScene crear, y la cutScene
            #a su vez tiene el control de que fase llevar.
            
        self.pila.append(menu)
    
    def definirMenu(self,menu):
        self.menu = menu
    
    def cambiarEscena(self, escena):
        self.salirEscena()
        # Ponemos la escena pasada en la cima de la pila
        self.pila.append(escena)
    

    def apilarEscena(self, escena):
        self.salir_escena = True
        # Ponemos la escena pasada en la cima de la pila
        #  (por encima de la actual)
        self.pila.append(escena)
    
    # --- Menu Pausa ---
    def escenaPausada(self,fase):
        self.fase = fase
    
    def devolverEscenaPausada(self):
        return self.fase
    
    def devolverHoraReloj(self):
        return self.reloj
    
        
