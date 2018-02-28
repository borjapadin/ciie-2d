#Importacion modulos
import pygame, sys
from pygame.locals import *

#Constantes
ANCHO_PANTALLA = 800
ALTO_PANTALLA = 600

BLANCO  = (255,255,255)

if __name__ == '__main__':

	#Inicializar pygame
	pygame.init()

	#Crear la pantalla
	pantalla = pygame.display.set_mode((ANCHO_PANTALLA,ALTO_PANTALLA),0,32)

	#Rellenamos pantalla color negro
	pantalla.fill((0,0,0))

	pygame.draw.circle(pantalla, BLANCO, (50,50),4,0)

	pygame.display.update()

	pygame.quit()
	sys.exit()
