# -*- encoding: utf-8 -*-
import pygame, sys, os
from pygame.locals import *
from escena import *
from gestorRecursos import *
from personajes import *
from inventario import *


class Objetos(MiSprite):
    "Cualquier objeto del juego"

    # Parametros pasados al constructor de esta clase:
    #  Archivo con la hoja de Sprites
    #  Archivo con las coordenadoas dentro de la hoja
    #  Numero de imagenes en cada postura
    #  Velocidad de caminar y de salto
    #  Retardo para mostrar la animacion del personaje
    def __init__(self, archivoImagen, primerParametroRect, top, left):

        # Primero invocamos al constructor de la clase padre
        MiSprite.__init__(self)
        self.primerParametroRect = primerParametroRect
        self.top = top
        self.left = left
        # Se carga la hoja
        self.cambiarImagen(archivoImagen)
        
    def cambiarImagen(self,archivoImagen):
        self.hoja = GestorRecursos.CargarImagen(archivoImagen,-1)
        self.hoja = self.hoja.convert_alpha()
    
        # El rectangulo del Sprite
        self.rect = pygame.Rect(self.primerParametroRect,[self.top,self.left])
        self.image = self.hoja.subsurface(0,0,self.top,self.left)        
    
    def obtenerObjeto():
        return imagen
    

class ObjetoPrincipal(Objetos):
    def __init__(self,imagen,posicionInventario):
        self.imagen = imagen
        self.posicionInventario = posicionInventario
        direccionImagen = 'Inventario/'+imagen+'.png'
        Objetos.__init__(self,direccionImagen,(0,20),34,40)
    
    def crearObjetoInventario(self,imagen):
        return ObjetoInventario(self.posicionInventario,self.imagen)


class KitCuracion(Objetos):
    def __init__(self,valorCurativo):
        self.valorCurativo = valorCurativo 
        Objetos.__init__(self,'Inventario/kitCurativo.png',(0,20),34,40)
    
    def getValorCurativo(self):
        return self.valorCurativo
    
    def vaciar(self):
        self.cambiarImagen('Inventario/kitCurativoVacio.png')
        self.valorCurativo = 0
        
    def recogerKitCurativo(self):
        valorCurativo = self.getValorCurativo()
        return valorCurativo

class PlataformaSecundaria(Objetos):
    def __init__(self,imagen):
        imagen = 'Caja.png' #CACA GRANDE
        Objetos.__init__(self,'PlataformasSecundarias/'+imagen,(0,35),63,50) 

    

    

