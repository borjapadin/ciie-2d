# -*- encoding: utf-8 -*-
from constantes import *
from gestorRecursos import *
from elementosDibujables import *


class Tiempo(ElementoDibujable):

    def __init__(self, inicial):

        unidades = inicial/10
        decena = inicial % 10
        self.tiempoTotal = inicial

        self.listaNumerosIzquierdos1 = []
        self.listaNumerosIzquierdos2 = []
        self.listaNumerosDerechos1 = []
        self.listaNumerosDerechos2 = []
        # Append de todos los números que hay para poder mostrarlos si hacen
        # falta.
        for i in range(0, 10):
            self.listaNumerosIzquierdos1.append(Numero(i, (675, 75)))
            self.listaNumerosIzquierdos2.append(Numero(i, (700, 75)))
            self.listaNumerosDerechos1.append(Numero(i, (725, 75)))
            self.listaNumerosDerechos2.append(Numero(i, (750, 75)))

        self.mostrarNumeroIzquierdo1(0)
        self.mostrarNumeroIzquierdo2(0)
        self.mostrarNumeroDerecho1(decena)
        self.mostrarNumeroDerecho2(unidades)

    def mostrarNumeroIzquierdo1(self, num):
        self.numeroIzquierdo1 = self.listaNumerosIzquierdos1[num]

    def mostrarNumeroIzquierdo2(self, num):
        self.numeroIzquierdo2 = self.listaNumerosIzquierdos2[num]

    def mostrarNumeroDerecho1(self, num):
        self.numeroDerecho1 = self.listaNumerosDerechos1[num]

    def mostrarNumeroDerecho2(self, num):
        self.numeroDerecho2 = self.listaNumerosDerechos2[num]

    def dibujar(self, pantalla):
        self.numeroDerecho1.dibujar(pantalla)
        self.numeroDerecho2.dibujar(pantalla)
        self.numeroIzquierdo1.dibujar(pantalla)
        self.numeroIzquierdo2.dibujar(pantalla)

    def establecerPosicion(self, posicion):
        (posicionx, posiciony) = posicion
        self.rect.left = posicionx
        self.rect.bottom = posiciony

    def actualizarCronometro(self, tiempo):
        tiempoInvertido = abs(tiempo-self.tiempoTotal)
        print(tiempoInvertido)
        self.mostrarNumeroDerecho1(tiempoInvertido/10)
        self.mostrarNumeroDerecho2(tiempoInvertido % 10)
        

class Numero:

    def __init__(self, numero, posicion):
        self.imagen = GestorRecursos.CargarImagen(
            'Tiempo/' + str(numero) + '.png', -1)
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
