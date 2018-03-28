# -*- encoding: utf-8 -*-
from constantes import *
from gestorRecursos import *
from elementosDibujables import *


class Tiempo(ElementoDibujable):

    def __init__(self, inicial):
        self.stringinicial = ["0","0","0","0"]

        self.tiempoTotal = inicial

        self.averiguarTiempo(self.tiempoTotal)
        self.listaNumeros = [[],[],[],[]]
       
        # Append de todos los números que hay para poder mostrarlos si hacen
        # falta.
        for i in range(0, 10):
            self.listaNumeros[0].append(Numero(i, (675, 75)))
            self.listaNumeros[1].append(Numero(i, (700, 75)))
            self.listaNumeros[2].append(Numero(i, (725, 75)))
            self.listaNumeros[3].append(Numero(i, (750, 75)))

        self.numeroMostrado = [[],[],[],[]]
        self.mostrarTodosLosNumeros()
    
    def mostrarTodosLosNumeros(self):
        for i in range(0,4):
            self.mostrarNumeroMostrado(i,self.stringinicial[i])

    def averiguarTiempo(self,tiempo):
        lista = list(str(tiempo))[::-1] #Hacerlo reverse por el tema de que no se llenan 4/4 casillas
        incremento = 4-len(lista)#Puede no empezar desde el inicio si es menor de 1000 así que calculo diferencia.
        for index in range(0,4):
            try:
                self.stringinicial[index] = lista[index] 
            except IndexError:
                self.stringinicial[index] = "0" #Si se pasa es que son ceros.
        self.stringinicial = self.stringinicial[::-1] #Reversearla.
    
    def mostrarNumeroMostrado(self,numero,num):
        self.numeroMostrado[numero] = self.listaNumeros[numero][int(num)]

    def dibujar(self, pantalla):
        for i in range(0,4):
            self.numeroMostrado[i].dibujar(pantalla)
    
    def establecerPosicion(self, posicion):
        (posicionx, posiciony) = posicion
        self.rect.left = posicionx
        self.rect.bottom = posiciony

    def actualizarCronometro(self, tiempo):
        tiempoInvertido = abs(tiempo-self.tiempoTotal)
        self.averiguarTiempo(tiempoInvertido)
        self.mostrarTodosLosNumeros()
        self.establecerTiempo(tiempoInvertido)

    def establecerTiempo(self,cronometro):
        self.tiempoCronometro = cronometro
    
    def obtenerTiempo(self):
        return self.tiempoCronometro


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
