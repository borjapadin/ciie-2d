# -*- encoding: utf-8 -*-
import pygame, sys, os
from pygame.locals import *
from escena import *
from gestorRecursos import *
from personajes import *
from inventario import *
#----------------------------
class Objetos(MiSprite):
    "Cualquier objeto del juego"

    # Parametros pasados al constructor de esta clase:
    #  Archivo con la hoja de Sprites
    #  Archivo con las coordenadoas dentro de la hoja
    #  Numero de imagenes en cada postura
    #  Velocidad de caminar y de salto
    #  Retardo para mostrar la animacion del personaje
    def __init__(self, archivoImagen, archivoCoordenadas):

        # Primero invocamos al constructor de la clase padre
        MiSprite.__init__(self);

        # Se carga la hoja
        self.hoja = GestorRecursos.CargarImagen(archivoImagen,-1)
        self.hoja = self.hoja.convert_alpha()
       
        # Leemos las coordenadas de un archivo de texto
        # No lo uso que no tengo ni idea de como funciona.
        #datos = GestorRecursos.CargarArchivoCoordenadas(archivoCoordenadas) 
        #datos = datos.split()

        # El rectangulo del Sprite
        self.rect = pygame.Rect((0,20),[34,40])
        self.image = self.hoja.subsurface(0,0,34,40)
    
    def obtenerObjeto():
        return imagen
    
class ObjetoPrincipal(Objetos):
    def __init__(self,imagen,archivoCoordenadas):
        self.imagen = imagen
        direccionImagen = 'Fase/1/Objetos/'+imagen+'.png'
        Objetos.__init__(self,direccionImagen,archivoCoordenadas)
    
    def crearObjetoInventario(self,num):
        return ObjetoInventario(num,self.imagen)
        

    

