# -*- encoding: utf-8 -*-
from constantes import *
from gestorRecursos import *

class Inventario:
        def __init__ (self):
                self.listObjetos = []
    
        def dibujar(self, pantalla):
                for objeto in self.listObjetos:
                        objeto.dibujar(pantalla)  
    
        def guardarObjeto(self,imagen):

class ObjetoInventario:
        def __init__(self,imagen):
                
    