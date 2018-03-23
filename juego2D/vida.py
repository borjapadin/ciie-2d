# -*- encoding: utf-8 -*-
from constantes import *
from gestorRecursos import *

class listaVidas:
    def __init__(self):
        self.listaVidas = []
        
        posicionVertical = 115
        for i in range(0,10):
            posicionVertical += 30
            self.listaVidas.append(Vida(posicionVertical,100))
    
    def dibujar(self,pantalla):
        for vida in self.listaVidas:
            vida.dibujar(pantalla)
    
    def perderVida(self,vidaPerdida):
        vida = self.listaVidas.pop()
        valorVida = vida.getValor()
        if vidaPerdida < valorVida: #Una bala lo máximo que va a quitar es una vida entera.
            valorVidaNueva = valorVida-vidaPerdida
            self.listaVidas.append(Vida(vida.posicionX(),valorVidaNueva))
    
class Vida:
    def __init__ (self,x,valor):
        self.valor = valor #Más natural guardar imagenes como múltiplos de 10 que de 1
        self.x = x
        self.cargarImagen()
    
    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, self.rect, self.rectSubimagen)	
    
    def cargarImagen(self):        
        objetoVidaImagen = 'Vida' + str(self.valor) + '.png'
        self.imagen = GestorRecursos.CargarImagen('Vida/'+objetoVidaImagen, -1)
        self.rect = self.imagen.get_rect()
        self.rect.bottom = ALTO_PANTALLA
    
        # La subimagen que estamos viendo
        self.rectSubimagen = pygame.Rect(0, 0, ANCHO_PANTALLA, ALTO_PANTALLA)
        self.establecerPosicion((self.x,80))        
    
    def establecerPosicion(self, posicion):
        (posicionx, posiciony) = posicion
        self.rect.left = posicionx
        self.rect.bottom = posiciony    
    
    def getValor(self):
        return self.valor
    
    def posicionX(self):
        return self.x