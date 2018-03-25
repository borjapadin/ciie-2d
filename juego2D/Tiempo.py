# -*- encoding: utf-8 -*-
from constantes import *
from gestorRecursos import *
from ElementosDibujables import *

class Tiempo(ElementoDibujable):
    def __init__ (self,inicial):
        
        self.listaNumerosIzquierdos = []
        self.listaNumerosDerechos = []
        #Append de todos los números que hay para poder mostrarlos si hacen falta.
        for i in range(0,10):
            self.listaNumerosIzquierdos.append(Numero(i,(700,75)))
            self.listaNumerosDerechos.append(Numero(i,(725,75)))
            
        self.mostrarNumeroIzquierdo(0)
        self.mostrarNumeroDerecho(0)
       
    def mostrarNumeroIzquierdo(self,num):
        self.numeroIzquierdo = self.listaNumerosIzquierdos[num]
       
    def mostrarNumeroDerecho(self,num):
        self.numeroDerecho = self.listaNumerosDerechos[num]
    
  
    def dibujar(self,pantalla):
        self.numeroDerecho.dibujar(pantalla)
        self.numeroIzquierdo.dibujar(pantalla)
    
    def establecerPosicion(self, posicion):
        (posicionx, posiciony) = posicion
        self.rect.left = posicionx
        self.rect.bottom = posiciony    
        
class Numero:
    
    def __init__(self,numero,posicion):
        self.imagen = GestorRecursos.CargarImagen('Tiempo/'+str(numero)+'.png', -1)
        self.rect = self.imagen.get_rect()
        self.rect.bottom = ALTO_PANTALLA
        
        self.rectSubimagen = pygame.Rect(0, 0, ANCHO_PANTALLA, ALTO_PANTALLA)
        self.establecerPosicion(posicion)                
    
    def devolverImagen(self):
        return self.imagen
    
    def devolverValorNumero(self):
        return self.num
    
    def establecerPosicion(self, posicion):
        (posicionx, posiciony) = posicion
        self.rect.left = posicionx
        self.rect.bottom = posiciony    
        
    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, self.rect, self.rectSubimagen)	    