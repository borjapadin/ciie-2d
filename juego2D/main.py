#Importacion modulos
import pygame

#Constantes
ANCHO_PANTALLA = 800
ALTO_PANTALLA = 600

if __name__ == '__main__':

	#Inicializar pygame
	pygame.init()

	#Crear la pantalla
	pantalla = pygame.display.set_mode((ANCHO_PANTALLA,ALTO_PANTALLA),0,32)