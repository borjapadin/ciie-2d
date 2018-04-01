#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
import director
from director import *
from menu import *
from loggerCreator import *

if __name__ == '__main__':
    # Inicializamos la libreria de pygame
    logger = loggerCreator.getLogger('MainLogs','MainLogs.log')
    pygame.init()
    
    logger.info('Juego iniciado, se creará director')
    # Creamos el director
    director = Director()

    # Creamos la escena con la pantalla inicial y la de configuracion
    logger.info('Creando escena...')
    escena = Menu(director)

    # Le decimos al director que apile esta escena
    director.definirMenu(escena)
    director.apilarEscena(escena)

    # Y ejecutamos el juego
    logger.info('Ejecutando juego...')
    director.ejecutar()
    
    # Cuando se termine la ejecución, finaliza la librería
    logger.info('Juego finalizado')
    pygame.quit()
