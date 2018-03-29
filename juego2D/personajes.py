# -*- encoding: utf-8 -*-
import pygame
import sys
import os
import time
from pygame.locals import *
from escena import *
from gestorRecursos import *
from random import randint

GRAVEDAD = 0.003  # Píxeles / ms2
# Movimientos
QUIETO = 0
IZQUIERDA = 1
DERECHA = 2
ARRIBA = 3
ABAJO = 4
DISPARAR = 5

DISTANCIA_BALA = 150

VELOCIDAD_RECARGA_BALA_HEROE = 200
VELOCIDAD_RECARGA_BALA_SOLDADO = 60
VELOCIDAD_RECARGA_BALA_BOSS = 35
#Velocidad de la bala.
VELOCIDAD_BALA_BOSS = 4
VELOCIDAD_BALA_JUGADOR = 3
VELOCIDAD_BALA_SOLDADO = 2

ON = 1
OFF = 0

# Posturas
SPRITE_QUIETO = 0
SPRITE_ANDANDO = 1
SPRITE_SALTANDO = 2
SPRITE_DISPARANDO = 3
SPRITE_AGACHANDO = 4
SPRITE_MURIENDO = 5

# Velocidades protagonista
VELOCIDAD_JUGADOR = 0.2  # Pixeles por milisegundo
VELOCIDAD_SALTO_JUGADOR = 0.3  # Pixeles por milisegundo
RETARDO_ANIMACION_JUGADOR = 5  # updates que durará cada imagen del personaje
# debería de ser un valor distinto para cada postura
RETARDO_ANIMACION_JUGADOR_SALTAR = 20
# velocidades de enemigos
VELOCIDAD_SOLDADO = 0.12  # Pixeles por milisegundo
VELOCIDAD_ZOMBIE = 0.09
VELOCIDAD_SALTO_SOLDADO = 0.27  # Pixeles por milisegundo
RETARDO_ANIMACION_SOLDADO = 5  # updates que durará cada imagen del personaje
RETARDO_ANIMACION_ZOMBIE = 8
GRAVEDAD = 0.0006  # Píxeles / ms2
VELOCIDAD_BALAS = 5



class MiSprite(pygame.sprite.Sprite):
    "Los Sprites que tendra este juego"

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.posicion = (0, 0)
        self.velocidad = (0, 0)
        self.scroll = (0, 0)

    def establecerPosicion(self, posicion):
        self.posicion = posicion
        self.rect.left = self.posicion[0] - self.scroll[0]
        self.rect.bottom = self.posicion[1] - self.scroll[1]

    def establecerPosicionPantalla(self, scrollDecorado):
        self.scroll = scrollDecorado
        (scrollx, scrolly) = self.scroll
        (posx, posy) = self.posicion
        self.rect.left = posx - scrollx
        self.rect.bottom = posy - scrolly

    def incrementarPosicion(self, incremento):
        (posx, posy) = self.posicion
        (incrementox, incrementoy) = incremento
        self.establecerPosicion((posx + incrementox, posy + incrementoy))

    def update(self, tiempo):
        incrementox = self.velocidad[0] * tiempo
        incrementoy = self.velocidad[1] * tiempo
        self.incrementarPosicion((incrementox, incrementoy))



class Personaje(MiSprite):
    "Cualquier personaje del juego"

    # Parametros pasados al constructor de esta clase:
    #  Archivo con la hoja de Sprites
    #  Archivo con las coordenadoas dentro de la hoja
    #  Numero de imagenes en cada postura
    #  Velocidad de caminar y de salto
    #  Retardo para mostrar la animacion del personaje
    def __init__(self, archivoImagen, archivoCoordenadas, numImagenes, velocidadCarrera, velocidadSalto, retardoAnimacion):

        # Primero invocamos al constructor de la clase padre
        MiSprite.__init__(self)

        # Se carga la hoja
        self.hoja = GestorRecursos.CargarImagen(archivoImagen, -1)
        self.hoja = self.hoja.convert_alpha()
        # El movimiento que esta realizando
        self.movimiento = QUIETO

        self.archivoImagen = archivoImagen

        # Leemos las coordenadas de un archivo de texto
        datos = GestorRecursos.CargarArchivoCoordenadas(archivoCoordenadas)
        datos = datos.split()
        self.numPostura = 1
        self.numImagenPostura = 0
        cont = 0
        self.coordenadasHoja = []
        variable = 0

        if archivoImagen == 'Personajes/rossi.png':
            variable = 6
            self.mirando = DERECHA
        elif archivoImagen == 'Personajes/BossHorizontal.png':
            variable = 5
            self.mirando = IZQUIERDA
        elif archivoImagen == 'Personajes/SpriteSoldadoFilas.png':
            variable = 4
            self.mirando = IZQUIERDA
        elif archivoImagen == 'Personajes/Zombie.png':
            variable = 3
            self.mirando = IZQUIERDA


        for linea in range(0, variable):
            self.coordenadasHoja.append([])
            tmp = self.coordenadasHoja[linea]
            for postura in range(1, numImagenes[linea] + 1):
                tmp.append(pygame.Rect((int(datos[cont]), int(
                    datos[cont + 1])), (int(datos[cont + 2]), int(datos[cont + 3]))))
                cont += 4

        # El retardo a la hora de cambiar la imagen del Sprite (para que no se
        # mueva demasiado rápido)
        self.retardoMovimiento = 0

        # En que postura esta inicialmente
        self.numPostura = QUIETO

        # El rectangulo del Sprite
        self.rect = pygame.Rect(120, 120, self.coordenadasHoja[self.numPostura][self.numImagenPostura][
                                2], self.coordenadasHoja[self.numPostura][self.numImagenPostura][3])

        # Las velocidades de caminar y salto
        self.velocidadCarrera = velocidadCarrera
        self.velocidadSalto = velocidadSalto

        # El retardo en la animacion del personaje (podria y deberia ser
        # distinto para cada postura)
        self.retardoAnimacion = retardoAnimacion

        # Y actualizamos la postura del Sprite inicial, llamando al metodo
        # correspondiente
        self.actualizarPostura()

        self.count_disparar = 0

    def establecerVida(self, vida):
        self.vida = vida

    def perderVida(self, valor):
        self.vida -= valor

    def recuperarVida(self, valor):
        self.vida += valor
        if (self.vida > 1000):
            self.vida = 1000
    
    def tieneVida(self):
        return (self.vida > 0)
    
    def devolverVida(self):
        return self.vida
    
    def balasLanzar(self):
        return self.balas

    # Metodo base para realizar el movimiento: simplemente se le indica cual
    # va a hacer, y lo almacena
    def mover(self, movimiento):
        if movimiento == ARRIBA:
            # Si estamos en el aire y el personaje quiere saltar, ignoramos
            # este movimiento
            if self.numPostura == SPRITE_SALTANDO:
                self.movimiento = QUIETO
            else:
                self.movimiento = ARRIBA
        else:
            self.movimiento = movimiento

    def actualizarPostura(self):
        self.retardoMovimiento -= 1
        # Miramos si ha pasado el retardo para dibujar una nueva postura
        if (self.retardoMovimiento < 0):
            self.retardoMovimiento = self.retardoAnimacion
            # Si ha pasado, actualizamos la postura
            self.numImagenPostura += 1
            if self.numImagenPostura >= len(self.coordenadasHoja[self.numPostura]):
                self.numImagenPostura = 0
            if self.numImagenPostura < 0:
                self.numImagenPostura = len(
                    self.coordenadasHoja[self.numPostura]) - 1
            self.image = self.hoja.subsurface(
                self.coordenadasHoja[self.numPostura][self.numImagenPostura])

            # Si esta mirando a la izquiera, cogemos la porcion de la hoja
            if self.archivoImagen == 'Personajes/rossi.png':
                if self.mirando == DERECHA:
                    self.image = self.hoja.subsurface(
                        self.coordenadasHoja[self.numPostura][self.numImagenPostura])
                #  Si no, si mira a la derecha, invertimos esa imagen
                elif self.mirando == IZQUIERDA:
                    self.image = pygame.transform.flip(self.hoja.subsurface(
                        self.coordenadasHoja[self.numPostura][self.numImagenPostura]), 1, 0)
            else:
                if self.mirando == IZQUIERDA:
                    self.image = self.hoja.subsurface(
                        self.coordenadasHoja[self.numPostura][self.numImagenPostura])
                #  Si no, si mira a la derecha, invertimos esa imagen
                elif self.mirando == DERECHA:
                    self.image = pygame.transform.flip(self.hoja.subsurface(
                        self.coordenadasHoja[self.numPostura][self.numImagenPostura]), 1, 0)

    def update(self, grupoPlataformas, tiempo):

        # Las velocidades a las que iba hasta este momento
        (velocidadx, velocidady) = self.velocidad
        # Funcion que dispara una bala si esta t pulsado

        if self.numPostura == SPRITE_SALTANDO:
            self.retardoAnimacion = GRAVEDAD * 25000
        else:
            self.retardoAnimacion = 5

        # Si vamos a la izquierda o a la derecha
        if (self.movimiento == IZQUIERDA) or (self.movimiento == DERECHA):
            # Esta mirando hacia ese lado
            self.mirando = self.movimiento

            # Si vamos a la izquierda, le ponemos velocidad en esa dirección
            if self.movimiento == IZQUIERDA:
                velocidadx = -self.velocidadCarrera
            # Si vamos a la derecha, le ponemos velocidad en esa dirección
            else:
                velocidadx = self.velocidadCarrera

            # Si no estamos en el aire
            if self.numPostura != SPRITE_SALTANDO:
                # La postura actual sera estar caminando
                self.numPostura = SPRITE_ANDANDO
                # Ademas, si no estamos encima de ninguna plataforma, caeremos
                if pygame.sprite.spritecollideany(self, grupoPlataformas) == None:
                    self.numPostura = SPRITE_SALTANDO

        # Si queremos saltar
        elif self.movimiento == ARRIBA:
            # La postura actual sera estar saltando
            self.numPostura = SPRITE_SALTANDO
            # Le imprimimos una velocidad en el eje y
            velocidady = -self.velocidadSalto

        # elif self.movimiento == ABAJO:
         #   #velocidady += GRAVEDAD * tiempo
          #  self.numPostura = SPRITE_AGACHANDO

            #plataforma = pygame.sprite.spritecollideany(self, grupoPlataformas)
            # if plataforma.rect.bottom<self.rect.bottom:
            #self.establecerPosicion((self.posicion[0], 401))

        # Si no se ha pulsado ninguna tecla
        elif self.movimiento == QUIETO:
            # Si no estamos saltando, la postura actual será estar quieto
            if not self.numPostura == SPRITE_SALTANDO:
                self.numPostura = SPRITE_QUIETO
            velocidadx = 0
        elif self.movimiento == DISPARAR:
            # La postura actual sera estar saltando
            if self.numPostura != SPRITE_SALTANDO:
                if self.archivoImagen == 'Personajes/rossi.png':
                    self.decidirSiDisparar(tiempo)
                    velocidadx = 0
            else:
                self.decidirSiDisparar(tiempo)
                self.numPostura = SPRITE_SALTANDO
                self.retardoAnimacion = GRAVEDAD * 25000
        # Además, si estamos en el aire
        if self.numPostura == SPRITE_SALTANDO:

            # Miramos a ver si hay que parar de caer: si hemos llegado a una plataforma
            # Para ello, miramos si hay colision con alguna plataforma del
            # grupo
            plataforma = pygame.sprite.spritecollideany(self, grupoPlataformas)
            #  Ademas, esa colision solo nos interesa cuando estamos cayendo
            #  y solo es efectiva cuando caemos encima, no de lado, es decir,
            # cuando nuestra posicion inferior esta por encima de la parte de
            # abajo de la plataforma
            if (plataforma != None) and (velocidady > 0) and (plataforma.rect.bottom > self.rect.bottom):
                # Lo situamos con la parte de abajo un pixel colisionando con la plataforma
                #  para poder detectar cuando se cae de ella
                self.establecerPosicion((self.posicion[0], plataforma.posicion[
                                        1] - plataforma.rect.height + 1))
                # Lo ponemos como quieto
                self.numPostura = SPRITE_QUIETO
                # Y estará quieto en el eje y
                velocidady = 0

            # Si no caemos en una plataforma, aplicamos el efecto de la
            # gravedad
            else:
                velocidady += GRAVEDAD * tiempo
        if self.archivoImagen != 'Personajes/Zombie.png':
            self.crearBala()
        # Actualizamos la imagen a mostrar
        self.actualizarPostura()

        # Aplicamos la velocidad en cada eje
        self.velocidad = (velocidadx, velocidady)

        # Y llamamos al método de la superclase para que, según la velocidad y el tiempo
        #  calcule la nueva posición del Sprite
        MiSprite.update(self, tiempo)

        return




class Pistolero():

    def __init__(self):
        self.inicializarBalas()

    def inicializarBalas(self):
        self.balas = None

    def vaciarPistola(self):
        self.disparar = OFF
        return self.balas
    
    def determinarVelocidadBala(self,velocidad):
        self.velocidadBala = velocidad

    def obtenerVelocidadBala(self):
        return self.velocidadBala

    def vaciarBalas(self):
        self.balas = None

    def inicializarCountDisparar(self):
        self.count_disparar = 0

    def aumentarContadorDisparo(self):
        self.count_disparar += 1

    def tieneBalas(self):
        return (self.balas != None)

    def balasLanzar(self):
        return self.balas

    def crearBala(self):
        # Si se ha pulsado que quieres disparar
        pupita = 0
        if self.disparar == ON:
            if self.archivoImagen == 'Personajes/rossi.png':
                pupita = 20
            elif self.archivoImagen == 'Personajes/SpriteSoldadoFilas.png':
                pupita = 40
            else:
                pupita = 80
            self.bala = BalaHeroe('Personajes/playerBullet.png',
                                  'Personajes/offsetBala.txt', self.obtenerVelocidadBala(), 1, pupita)
            self.disparar = OFF
            if self.archivoImagen == 'Personajes/rossi.png':
                if self.mirando == IZQUIERDA:
                    self.bala.establecerPosicion(
                        (self.posicion[0] - 10, self.posicion[1] - 21))
                else:
                    # Ponemos la bala en la posicion actual del heroe.
                    self.bala.establecerPosicion(
                        (self.posicion[0] + 40, self.posicion[1] - 21))
                self.balas = self.bala
            else:
                if self.mirando == IZQUIERDA:
                    self.bala.establecerPosicion(
                        (self.posicion[0] - 10, self.posicion[1] - 21))
                else:
                    # Ponemos la bala en la posicion actual del heroe.
                    self.bala.establecerPosicion(
                        (self.posicion[0] + 40, self.posicion[1] - 21))
                self.balas = self.bala




class Jugador(Pistolero, Personaje):
    "Cualquier personaje del juego"

    def __init__(self,vidaActual=1000): #Vida Actual = 1000 si no se dice nada
        # Invocamos al constructor de la clase padre con la configuracion de
        # este personaje concreto
        Personaje.__init__(self, 'Personajes/rossi.png', 'Personajes/offsetRossi.txt', [
                           1, 7, 5, 6, 8, 6], VELOCIDAD_JUGADOR, VELOCIDAD_SALTO_JUGADOR, RETARDO_ANIMACION_JUGADOR)
        self.disparar = OFF
        self.inicializarBalas()
        self.determinarVelocidadBala(VELOCIDAD_BALA_JUGADOR)
        self.count_disparar = 150
        self.establecerVida(vidaActual)

    def mover(self, teclasPulsadas, arriba, abajo, izquierda, derecha, disparar):
        # Indicamos la acción a realizar segun la tecla pulsada para el jugador

        if teclasPulsadas[arriba]:
            Personaje.mover(self, ARRIBA)
        elif teclasPulsadas[izquierda]:
            Personaje.mover(self, IZQUIERDA)
        elif teclasPulsadas[derecha]:
            Personaje.mover(self, DERECHA)
        elif teclasPulsadas[abajo]:
            Personaje.mover(self, ABAJO)
        elif teclasPulsadas[disparar]:
            self.disparar = ON
            Personaje.mover(self, DISPARAR)
        else:
            Personaje.mover(self, QUIETO)

    def decidirSiDisparar(self, tiempo):
        if (self.count_disparar >= VELOCIDAD_RECARGA_BALA_HEROE):
            self.dispararBala()
            self.inicializarCountDisparar()
            self.numPostura = SPRITE_DISPARANDO
        else:
            self.aumentarContadorDisparo(tiempo)
            self.disparar = OFF

    # Override
    def inicializarCountDisparar(self):
        self.count_disparar = 0
        self.disparado = 0

    # Override
    def aumentarContadorDisparo(self, tiempo):
        self.count_disparar += tiempo

    # Override
    def dispararBala(self):
        self.disparar = ON
        Personaje.mover(self, DISPARAR)



class NoJugador(Personaje):
    "El resto de personajes no jugadores"

    def __init__(self, archivoImagen, archivoCoordenadas, numImagenes, velocidad, velocidadSalto, retardoAnimacion):
        # Primero invocamos al constructor de la clase padre con los parametros
        # pasados
        self.esJefe = False
        Personaje.__init__(self, archivoImagen, archivoCoordenadas,
                           numImagenes, velocidad, velocidadSalto, retardoAnimacion)
        
    # Aqui vendria la implementacion de la IA segun las posiciones de los jugadores
    # La implementacion por defecto, este metodo deberia de ser implementado en las clases inferiores
    #  mostrando la personalidad de cada enemigo
    def esUnJefe(self):
        return self.esJefe

    
class Zombie(NoJugador):
    def __init__(self):
        NoJugador.__init__(self, 'Personajes/Zombie.png', 'Personajes/OffsetZombie.txt', [
                            1, 6, 4], VELOCIDAD_ZOMBIE, VELOCIDAD_SALTO_SOLDADO, RETARDO_ANIMACION_SOLDADO)
        self.establecerVida(20)
        self.damage = 10

    def mover_cpu(self, jugador, tiempo):
        if self.rect.left > 0 and self.rect.right < ANCHO_PANTALLA and self.rect.bottom > 0 and self.rect.top < ALTO_PANTALLA:
            if jugador.posicion[0] < self.posicion[0]:
                self.mirando = IZQUIERDA
                Personaje.mover(self, IZQUIERDA)
            else:
                self.mirando = DERECHA
                Personaje.mover(self, DERECHA)
        else:
            Personaje.mover(self,QUIETO)

    def damageEnemigo(self):
        return self.damage




class Soldado(Pistolero, NoJugador):
    def __init__(self):
        NoJugador.__init__(self, 'Personajes/SpriteSoldadoFilas.png', 'Personajes/offsetsSoldado.txt', [
                           1, 9, 8, 8], VELOCIDAD_SOLDADO, VELOCIDAD_SALTO_SOLDADO, RETARDO_ANIMACION_SOLDADO)
        self.establecerVida(80)
        self.inicializarBalas()
        self.determinarVelocidadBala(VELOCIDAD_BALA_SOLDADO)
        self.damage = 10
        self.disparar = OFF
        self.inicializarCountDisparar()

    def mover_cpu(self, jugador, tiempo):
        if self.rect.left > 0 and self.rect.right < ANCHO_PANTALLA and self.rect.bottom > 0 and self.rect.top < ALTO_PANTALLA:
            #self.decidirSiDisparar()
            #-----------------------------Mirar-----------------------------
            #if self.movimiento == DISPARAR:
            posicionJugador = jugador.posicion[0] 
            posicionEnemigo = self.posicion[0]
            
            if posicionJugador < posicionEnemigo:
                if (posicionEnemigo-posicionJugador) < 200: #La distancia es menor de 50
                    if (self.count_disparar >= VELOCIDAD_RECARGA_BALA_SOLDADO): #Velocidad recarga bala.
                        self.mirando = IZQUIERDA            
                        self.numPostura = SPRITE_DISPARANDO
                        self.disparar = ON
                        Personaje.mover(self, DISPARAR)
                        self.inicializarCountDisparar()
                    else:
                        self.aumentarContadorDisparo()
                else: 
                    Personaje.mover(self,QUIETO)
            elif posicionEnemigo < posicionJugador:
                if (posicionJugador-posicionEnemigo) < 200: #La distancia es menor de 50 
                    if (self.count_disparar >= VELOCIDAD_RECARGA_BALA_SOLDADO): #Velocidad recarga bala.
                        self.mirando = DERECHA
                        self.numPostura = SPRITE_DISPARANDO
                        self.disparar = ON
                        Personaje.mover(self, DISPARAR)
                        self.inicializarCountDisparar()
                    else:
                        self.disparar = OFF
                        self.aumentarContadorDisparo()
                else:
                    Personaje.mover(self,QUIETO)
            else:
                Personaje.mover(self,QUIETO)

    def damageEnemigo(self):
        return self.damage

    def decidirSiDisparar(self):
        if (self.count_disparar == VELOCIDAD_RECARGA_BALA):
            self.dispararBala()
            self.inicializarCountDisparar()
            Personaje.numPostura = SPRITE_DISPARANDO
        else:
            self.aumentarContadorDisparo()

    def dispararBala(self):
        # Vamos a meterle aletoriedad para que no sea tan mecanico y resulte
        # más natural.
        self.disparar = randint(OFF, ON)
        Personaje.mover(self, DISPARAR)


class Boss(Pistolero, NoJugador):
    def __init__(self):
        NoJugador.__init__(self, 'Personajes/BossHorizontal.png', 'Personajes/offsetsMalo.txt', [
                           1, 7, 6, 2, 8], VELOCIDAD_SOLDADO, VELOCIDAD_SALTO_SOLDADO, RETARDO_ANIMACION_SOLDADO)
        self.establecerVida(400)
        self.inicializarBalas()
        self.determinarVelocidadBala(VELOCIDAD_BALA_BOSS)
        self.damage = 20
        self.disparar = OFF
        self.inicializarCountDisparar()
        self.esJefe = True

    def mover_cpu(self, jugador, tiempo):
        if self.rect.left > 0 and self.rect.right < ANCHO_PANTALLA and self.rect.bottom > 0 and self.rect.top < ALTO_PANTALLA:
            #self.decidirSiDisparar()
            #-----------------------------Mirar-----------------------------
            #if self.movimiento == DISPARAR:
            posicionJugador = jugador.posicion[0] 
            posicionEnemigo = self.posicion[0]
            if posicionJugador < posicionEnemigo:
                if (posicionEnemigo-posicionJugador) < 350: #La distancia es menor de 50
                    if (self.count_disparar >= VELOCIDAD_RECARGA_BALA_BOSS): #Velocidad recarga bala.          
                        self.mirando = IZQUIERDA
                        self.numPostura = SPRITE_DISPARANDO
                        self.disparar = ON
                        Personaje.mover(self, IZQUIERDA)
                        Personaje.mover(self, DISPARAR)
                        self.inicializarCountDisparar()
                    else:
                        self.aumentarContadorDisparo()
                else: 
                    Personaje.mover(self,IZQUIERDA)
            elif posicionEnemigo < posicionJugador:
                if (posicionJugador-posicionEnemigo) < 350: #La distancia es menor de 50 
                    if (self.count_disparar >= VELOCIDAD_RECARGA_BALA_BOSS): #Velocidad recarga bala.
                        self.mirando = DERECHA
                        self.numPostura = SPRITE_DISPARANDO
                        self.disparar = ON
                        #Personaje.mover(self, DERECHA)
                        Personaje.mover(self, DISPARAR)
                        self.inicializarCountDisparar()
                    else:
                        self.disparar = OFF
                        self.aumentarContadorDisparo()
                else:
                    Personaje.mover(self,DERECHA)
            else:
                Personaje.mover(self,QUIETO)
        elif self.rect.left > 0:
            Personaje.mover(self,IZQUIERDA)
        else:
            Personaje.mover(self,DERECHA)

    def damageEnemigo(self):
        return self.damage

    def decidirSiDisparar(self):
        if (self.count_disparar == VELOCIDAD_RECARGA_BALA):
            self.dispararBala()
            self.inicializarCountDisparar()
            Personaje.numPostura = SPRITE_DISPARANDO
        else:
            self.aumentarContadorDisparo()

    def dispararBala(self):
        # Vamos a meterle aletoriedad para que no sea tan mecanico y resulte
        # más natural.
        self.disparar = randint(OFF, ON)
        Personaje.mover(self, DISPARAR)


class BalaHeroe(MiSprite):
    def __init__(self, archivoImagen, archivoCoordenadas, velocidad, direccion, pupa):

        MiSprite.__init__(self)
        
        self.distancia = 0

        self.mirando = direccion
        self.damage = pupa  # De momento por defecto porque me da pereza buscar

        self.velocidad = velocidad
        self.retardoAnimacion = 5  # No le pondría el retardo de la animación.

        self.hoja = GestorRecursos.CargarImagen(archivoImagen, -1)
        self.hoja.convert_alpha()
        # Carga un rectángulo en el cual va a dibujar la imagen.
        self.rect = pygame.Rect((5, 20), [7, 7])
        self.image = self.hoja.subsurface(0, 0, 7, 7)

        self.mirando = 0

    def obtenermovimiento(self, jugador):
        self.mirando = jugador.mirando

    def moverBala(self):
        if self.distancia < DISTANCIA_BALA:
            if self.mirando == DERECHA:
                # jojoojjojoojoj... efecto rayo laser!!
                self.incrementarPosicion((self.velocidad, 0))
            else:
                self.incrementarPosicion((-self.velocidad, 0))
            self.distancia += abs(self.velocidad)
        else:
            self.destruirBala()

    def destruirBala(self):
        self.kill()

    def damageBala(self):
        return self.damage