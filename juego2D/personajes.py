# -*- encoding: utf-8 -*-
import pygame, sys, os
from pygame.locals import *
from escena import *
from gestorRecursos import *

# Constantes--------------
GRAVEDAD = 0.003 # Píxeles / ms2
# Movimientos
QUIETO = 0
IZQUIERDA = 1
DERECHA = 2
ARRIBA = 3
ABAJO = 4
DISPARAR = 5

#Posturas
SPRITE_QUIETO = 0
SPRITE_ANDANDO = 1
SPRITE_SALTANDO = 2
SPRITE_DISPARANDO = 3
SPRITE_AGACHANDO = 4
SPRITE_MURIENDO = 5

# Velocidades protagonista
VELOCIDAD_JUGADOR = 0.2 # Pixeles por milisegundo
VELOCIDAD_SALTO_JUGADOR = 0.3 # Pixeles por milisegundo
RETARDO_ANIMACION_JUGADOR = 5 # updates que durará cada imagen del personaje
                              # debería de ser un valor distinto para cada postura
RETARDO_ANIMACION_JUGADOR_SALTAR = 20
# velocidades de enemigos
VELOCIDAD_SNIPER = 0.12 # Pixeles por milisegundo
VELOCIDAD_SALTO_SNIPER = 0.27 # Pixeles por milisegundo
RETARDO_ANIMACION_SNIPER = 5 # updates que durará cada imagen del personaje

GRAVEDAD = 0.0006 # Píxeles / ms2

#----------------------------
# Clase MiSprite
class MiSprite(pygame.sprite.Sprite):
    "Los Sprites que tendra este juego"
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.posicion = (0, 0)
        self.velocidad = (0, 0)
        self.scroll   = (0, 0)

    def establecerPosicion(self, posicion):
        self.posicion = posicion
        self.rect.left = self.posicion[0] - self.scroll[0]
        self.rect.bottom = self.posicion[1] - self.scroll[1]

    def establecerPosicionPantalla(self, scrollDecorado):
        self.scroll = scrollDecorado;
        (scrollx, scrolly) = self.scroll;
        (posx, posy) = self.posicion;
        self.rect.left = posx - scrollx;
        self.rect.bottom = posy - scrolly;

    def incrementarPosicion(self, incremento):
        (posx, posy) = self.posicion
        (incrementox, incrementoy) = incremento
        self.establecerPosicion((posx+incrementox, posy+incrementoy))

    def update(self, tiempo):
        incrementox = self.velocidad[0]*tiempo
        incrementoy = self.velocidad[1]*tiempo
        self.incrementarPosicion((incrementox, incrementoy))

#---------------------------
# Clases Personaje
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
        MiSprite.__init__(self);

        # Se carga la hoja
        self.hoja = GestorRecursos.CargarImagen(archivoImagen,-1)
        self.hoja = self.hoja.convert_alpha()
        # El movimiento que esta realizando
        self.movimiento = QUIETO
        # Lado hacia el que esta mirando
        self.mirando = DERECHA

        # Leemos las coordenadas de un archivo de texto
        datos = GestorRecursos.CargarArchivoCoordenadas(archivoCoordenadas)
        datos = datos.split()
        self.numPostura = 1;
        self.numImagenPostura = 0;
        cont = 0;
        self.coordenadasHoja = [];
        for linea in range(0, 6):
            self.coordenadasHoja.append([])
            tmp = self.coordenadasHoja[linea]
            for postura in range(1, numImagenes[linea]+1):
                tmp.append(pygame.Rect((int(datos[cont]), int(datos[cont+1])), (int(datos[cont+2]), int(datos[cont+3]))))
                cont += 4

        # El retardo a la hora de cambiar la imagen del Sprite (para que no se mueva demasiado rápido)
        self.retardoMovimiento = 0;

        # En que postura esta inicialmente
        self.numPostura = QUIETO

        # El rectangulo del Sprite
        self.rect = pygame.Rect(100,100,self.coordenadasHoja[self.numPostura][self.numImagenPostura][2],self.coordenadasHoja[self.numPostura][self.numImagenPostura][3])

        # Las velocidades de caminar y salto
        self.velocidadCarrera = velocidadCarrera
        self.velocidadSalto = velocidadSalto

        # El retardo en la animacion del personaje (podria y deberia ser distinto para cada postura)
        self.retardoAnimacion = retardoAnimacion

        # Y actualizamos la postura del Sprite inicial, llamando al metodo correspondiente
        self.actualizarPostura()


    # Metodo base para realizar el movimiento: simplemente se le indica cual va a hacer, y lo almacena
    def mover(self, movimiento):
        if movimiento == ARRIBA:
            # Si estamos en el aire y el personaje quiere saltar, ignoramos este movimiento
            if self.numPostura == SPRITE_SALTANDO:
                self.movimiento = QUIETO
            else:
                self.movimiento = ARRIBA
        elif movimiento == DISPARAR: #Si quieres disparar tienes que estar quieto (inicialmente)
            self.movimiento = DISPARAR
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
                self.numImagenPostura = 0;
            if self.numImagenPostura < 0:
                self.numImagenPostura = len(self.coordenadasHoja[self.numPostura])-1
            self.image = self.hoja.subsurface(self.coordenadasHoja[self.numPostura][self.numImagenPostura])

            # Si esta mirando a la izquiera, cogemos la porcion de la hoja
            if self.mirando == DERECHA:
                self.image = self.hoja.subsurface(self.coordenadasHoja[self.numPostura][self.numImagenPostura])
            #  Si no, si mira a la derecha, invertimos esa imagen
            elif self.mirando == IZQUIERDA:
                self.image = pygame.transform.flip(self.hoja.subsurface(self.coordenadasHoja[self.numPostura][self.numImagenPostura]), 1, 0)


    def update(self, grupoPlataformas, tiempo):

        # Las velocidades a las que iba hasta este momento
        (velocidadx, velocidady) = self.velocidad

        if self.numPostura == SPRITE_SALTANDO :
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

        #elif self.movimiento == ABAJO:
         #   #velocidady += GRAVEDAD * tiempo
          #  self.numPostura = SPRITE_AGACHANDO

            #plataforma = pygame.sprite.spritecollideany(self, grupoPlataformas)
            #if plataforma.rect.bottom<self.rect.bottom:
      #      self.establecerPosicion((self.posicion[0], 401))

        # Si no se ha pulsado ninguna tecla
        elif self.movimiento == QUIETO:
            # Si no estamos saltando, la postura actual será estar quieto
            if not self.numPostura == SPRITE_SALTANDO:
                self.numPostura = SPRITE_QUIETO
            velocidadx = 0
        
        # Si se ha pulsado que quieres disparar
        elif self.movimiento == DISPARAR:
            self.bala = BalaHeroe('Fase/1/MANCHONNEGRO.png','Fase/1/offsetRossi.txt', [1,7,5,6,8,6], 1)
            print('disparar')
            self.bala.establecerPosicion((5, 401)) #Ponemos la bala en la posicion actual del heroe.  



        # Además, si estamos en el aire
        if self.numPostura == SPRITE_SALTANDO:

            # Miramos a ver si hay que parar de caer: si hemos llegado a una plataforma
            #  Para ello, miramos si hay colision con alguna plataforma del grupo
            plataforma = pygame.sprite.spritecollideany(self, grupoPlataformas)
            #  Ademas, esa colision solo nos interesa cuando estamos cayendo
            #  y solo es efectiva cuando caemos encima, no de lado, es decir,
            #  cuando nuestra posicion inferior esta por encima de la parte de abajo de la plataforma
            if (plataforma != None) and (velocidady>0) and (plataforma.rect.bottom>self.rect.bottom):
                # Lo situamos con la parte de abajo un pixel colisionando con la plataforma
                #  para poder detectar cuando se cae de ella
                self.establecerPosicion((self.posicion[0], plataforma.posicion[1]-plataforma.rect.height+1))
                # Lo ponemos como quieto
                self.numPostura = SPRITE_QUIETO
                # Y estará quieto en el eje y
                velocidady = 0

            # Si no caemos en una plataforma, aplicamos el efecto de la gravedad
            else:
                velocidady += GRAVEDAD * tiempo

        # Actualizamos la imagen a mostrar
        self.actualizarPostura()

        # Aplicamos la velocidad en cada eje
        self.velocidad = (velocidadx, velocidady)

        # Y llamamos al método de la superclase para que, según la velocidad y el tiempo
        #  calcule la nueva posición del Sprite
        MiSprite.update(self, tiempo)

        return
#---------------------------
# Clase Jugador

class Jugador(Personaje):
    "Cualquier personaje del juego"
    def __init__(self):
        # Invocamos al constructor de la clase padre con la configuracion de este personaje concreto
        #Personaje.__init__(self,'Fase/1/Jugador.png','Fase/1/coordJugador.txt', [6,12,6], VELOCIDAD_JUGADOR, VELOCIDAD_SALTO_JUGADOR, RETARDO_ANIMACION_JUGADOR);
        Personaje.__init__(self,'Fase/1/rossi.png','Fase/1/offsetRossi.txt', [1,7,5,6,8,6], VELOCIDAD_JUGADOR, VELOCIDAD_SALTO_JUGADOR, RETARDO_ANIMACION_JUGADOR);

    def mover(self, teclasPulsadas, arriba, abajo, izquierda, derecha, disparar):
        # Indicamos la acción a realizar segun la tecla pulsada para el jugador
        if teclasPulsadas[arriba]:
            Personaje.mover(self,ARRIBA)
        elif teclasPulsadas[izquierda]:
            Personaje.mover(self,IZQUIERDA)
        elif teclasPulsadas[derecha]:
            Personaje.mover(self,DERECHA)
        elif teclasPulsadas[abajo]:
            Personaje.mover(self,ABAJO)
        elif teclasPulsadas[disparar]:
            Personaje.mover(self,DISPARAR)
        else:
            Personaje.mover(self,QUIETO)


#--------------------------------------------------
# Clase NoJugador
class NoJugador(Personaje):
    "El resto de personajes no jugadores"
    def __init__(self, archivoImagen, archivoCoordenadas, numImagenes, velocidad, velocidadSalto, retardoAnimacion):
        # Primero invocamos al constructor de la clase padre con los parametros pasados
        Personaje.__init__(self, archivoImagen, archivoCoordenadas, numImagenes, velocidad, velocidadSalto, retardoAnimacion);

    # Aqui vendria la implementacion de la IA segun las posiciones de los jugadores
    # La implementacion por defecto, este metodo deberia de ser implementado en las clases inferiores
    #  mostrando la personalidad de cada enemigo
    def mover_cpu(self, jugador1, jugador2):
        # Por defecto un enemigo no hace nada
        #  (se podria programar, por ejemplo, que disparase al jugador por defecto)
        return
#---------------------------
# Clase Zombi

#---------------------------
# Clase Soldado

#---------------------------
# Clase Jefe

#----------------------------
# Clase MiSpriteBala
class MiSpriteBala(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.posicion = (0, 0)
        self.velocidad = (0, 0)

    def establecerPosicion(self, posicion, personaje = None): #Yo creo que no hay que meterle personaje, con tal de saber la posición inicial ya va.
        self.posicion = posicion
        print(posicion)
    #    self.rect.left = personaje.posicion[0] - personaje.scroll[0]

    def incrementarPosicion(self, incremento):
        (posx, posy) = self.posicion
        (incrementox, incrementoy) = incremento
        self.establecerPosicion((posx+incrementox, posy+incrementoy))

    def update(self, tiempo):
        incrementox = self.velocidad[0]*tiempo
        incrementoy = self.velocidad[1]*tiempo
        self.incrementarPosicion((incrementox, incrementoy))

#---------------------------
# Clase BalaHeroe
class BalaHeroe(MiSpriteBala):

    def __init__(self, archivoImagen, archivoCoordenadas, velocidad, direccion):

        MiSpriteBala.__init__(self);

        self.mirando = direccion
        
        self.velocidad = velocidad #No le pondria la velocidad porque todas las balas tendran la misma (?)
        self.retardoAnimacion = 5 #No le pondría el retardo de la animación.
        
        
        self.hoja = GestorRecursos.CargarImagen(archivoImagen, -1)
        self.hoja.convert_alpha()        
        #Carga un rectángulo en el cual va a dibujar la imagen.
        self.rect = pygame.Rect((0,20),[30,30])
        self.image = self.hoja.subsurface(0,0,200,200)
        
        

    def update(self, tiempo, direccion):
        (velocidadx, velocidady) = self.velocidad

        if direccion == IZQUIERDA:
            self.image = self.hoja.subsurface()
