# -*- encoding: utf-8 -*-
from constantes import *
from gestorRecursos import *
from elementosDibujables import *

MAX_VIDA = 1000


class listaVidasGenerico(ElementoDibujable):
    def __init__(self,imagen):
        self.listaVidas = []
        self.imagen = imagen #Imagen del corazon que van a cargar.

    def devolverImagenCorazon(self):
        return self.imagen 
    
    def dibujar(self,pantalla):
        for vida in self.listaVidas:
            vida.dibujar(pantalla)

    def perderVida(self,vidaPerdida):
        if (len(self.listaVidas)>0):
            vida = self.listaVidas.pop()
            valorVida = vida.getValor()
            if vidaPerdida < valorVida: #Una bala lo máximo que va a quitar es una vida entera.
                valorVidaNueva = valorVida-vidaPerdida
                self.listaVidas.append(Vida(vida.posicionX(),self.y,valorVidaNueva,self.devolverImagenCorazon()))

class listaVidasEnemigo(listaVidasGenerico):
    def __init__(self):
        listaVidasGenerico.__init__(self,'VidaEnemigo')
        # Altura a la que esta el corazón
        self.y = 500
        #Cuantos corazones enteros tenemos que dibujar
        posicionVertical = 700
        for i in range(0,4):
            posicionVertical -= 30
            self.listaVidas.append(Vida(posicionVertical,self.y,100,self.devolverImagenCorazon())) #Primeros coraazones enteritos

class listaVidas(listaVidasGenerico):
    def __init__(self,vidaAcumulada):
        listaVidasGenerico.__init__(self,'Vida')
        # Altura a la que está el corazón
        self.y = 80
        #Cuantos corazones enteros tenemos que dibujar.
        corazonesLlenos = int(vidaAcumulada/100)

        posicionVertical = 115
        for i in range(0,corazonesLlenos):
            posicionVertical += 30
            self.listaVidas.append(Vida(posicionVertical,self.y,100,self.devolverImagenCorazon())) #Primeros corazones enteritos

        #Cuanto esta lleno el último corazón
        ultimoCachitoUltimoCorazon = vidaAcumulada % 100 
        if ultimoCachitoUltimoCorazon != 0:
            self.listaVidas.append(Vida(posicionVertical+30,self.y,ultimoCachitoUltimoCorazon,self.devolverImagenCorazon()))

    
    def dibujar(self,pantalla):
        for vida in self.listaVidas:
            vida.dibujar(pantalla)
    
    def perderVida(self,vidaPerdida):
        if (len(self.listaVidas)>0):
            vida = self.listaVidas.pop()
            valorVida = vida.getValor()
            if vidaPerdida < valorVida: #Una bala lo máximo que va a quitar es una vida entera.
                valorVidaNueva = valorVida-vidaPerdida
                self.listaVidas.append(Vida(vida.posicionX(),self.y,valorVidaNueva,'Vida'))
                
    def recuperarVida(self,vidaGanada):
        if (len(self.listaVidas)<=10 and len(self.listaVidas)>0):
            vida = self.listaVidas.pop()
            valorVida = vida.getValor()
            if vidaGanada <= 100:
                valorVidaNueva = valorVida+vidaGanada
                if valorVidaNueva > 100: 
                    valorVidaNueva = 100
                self.listaVidas.append(Vida(vida.posicionX(),self.y,valorVidaNueva,'Vida'))
   

class Vida:
    def __init__ (self,x,y,valor,imagen):
        self.valor = valor #Más natural guardar imagenes como múltiplos de 10 que de 1
        self.x = x
        self.y = y
        self.cargarImagen(imagen)
    
    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, self.rect, self.rectSubimagen)	
    
    def cargarImagen(self,imagen):        
        objetoVidaImagen = imagen + str(self.valor) + '.png'
        self.imagen = GestorRecursos.CargarImagen('Vida/'+objetoVidaImagen, -1)
        self.rect = self.imagen.get_rect()
        self.rect.bottom = ALTO_PANTALLA
    
        # La subimagen que estamos viendo
        self.rectSubimagen = pygame.Rect(0, 0, ANCHO_PANTALLA, ALTO_PANTALLA)
        self.establecerPosicion((self.x,self.y))        
    
    def establecerPosicion(self, posicion):
        (posicionx, posiciony) = posicion
        self.rect.left = posicionx
        self.rect.bottom = posiciony    
    
    def getValor(self):
        return self.valor
    
    def posicionX(self):
        return self.x