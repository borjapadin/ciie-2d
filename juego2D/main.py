#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Importar modulos
# -*- encoding: utf-8 -*-

import pygame
import director
from director import *
from menu import *

if __name__ == '__main__':
    

    # Inicializamos la libreria de pygame
    pygame.init()
    
    # Creamos el director
    director = Director()
    # Creamos la escena con la pantalla inicial y la de configuracion
    escena = Menu(director)
    # Le decimos al director que apile esta escena
    director.definirMenu(escena)
    director.apilarEscena(escena)
    # Y ejecutamos el juego
    director.ejecutar()
    # Cuando se termine la ejecución, finaliza la librería
    pygame.quit()
