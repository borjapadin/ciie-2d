#Importacion modulos
import pygame, sys
from pygame.locals import *

#Constantes
ANCHO_PANTALLA = 800
ALTO_PANTALLA = 600


#Inicializar pygame
pygame.init()

#Crear la pantalla
pantalla = pygame.display.set_mode((ANCHO_PANTALLA,ALTO_PANTALLA))

BLANCO  = (255,255,255)


while True:

	for evento in pygame.event.get():

		if evento.type == KEYDOWN and evento.key == K_ESCAPE:
			pygame.quit()
			sys.exit()	


	#Rellenamos pantalla color negro
	pantalla.fill((0,0,0))

	pygame.draw.circle(pantalla, BLANCO, (100,100),4,0)

	pygame.display.update()

	if evento.type == QUIT:
		pygame.quit()
		sys.exit()

