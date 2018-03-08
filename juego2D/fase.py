# -*- coding: utf-8 -*-

import pygame, escena
from escena import *
from personajes import *
from pygame.locals import *
#from animaciones import *

# -------------------------------------------------
# -------------------------------------------------
# Constantes
# -------------------------------------------------
# -------------------------------------------------

ULTIMA_FASE = 3

# Los bordes de la pantalla para hacer scroll horizontal
MINIMO_X_JUGADOR = 50
MAXIMO_X_JUGADOR = ANCHO_PANTALLA - MINIMO_X_JUGADOR

# -------------------------------------------------
# Clase Fase

class Fase(Escena):
    def __init__(self, director, numFase):

        # Habria que pasarle como parámetro el número de fase, a partir del cual se cargue
        #  un fichero donde este la configuracion de esa fase en concreto, con cosas como
        #   - Nombre del archivo con el decorado
        #   - Posiciones de las plataformas
        #   - Posiciones de los enemigos
        #   - Posiciones de inicio de los jugadores
        #  etc.
        # Y cargar esa configuracion del archivo en lugar de ponerla a mano, como aqui abajo
        # De esta forma, se podrian tener muchas fases distintas con esta clase

        self.numFase = str(numFase) #Necesito que sea string para ponerlo en la ruta.
        self.numFaseSiguiente = numFase+1 #Para saber el numero de la fase siguiente 
        
        # Primero invocamos al constructor de la clase padre
        Escena.__init__(self, director)

        # Creamos el decorado y el fondo
        self.decorado = Decorado("/"+self.numFase)
        self.fondo = Cielo("/"+self.numFase)

        # Que parte del decorado estamos visualizando
        self.scrollx = 0
        #  En ese caso solo hay scroll horizontal

        
   
    def update(self, tiempo):

        # Primero, se indican las acciones que van a hacer los enemigos segun como esten los jugadores
        #for enemigo in iter(self.grupoEnemigos):
        #    enemigo.mover_cpu(self.jugador1, self.jugador2)
        # Esta operación es aplicable también a cualquier Sprite que tenga algún tipo de IA
        # En el caso de los jugadores, esto ya se ha realizado

        # Actualizamos los Sprites dinamicos
        # De esta forma, se simula que cambian todos a la vez
        # Esta operación de update ya comprueba que los movimientos sean correctos
        #  y, si lo son, realiza el movimiento de los Sprites
        #self.grupoSpritesDinamicos.update(self.grupoPlataformas, tiempo)
        # Dentro del update ya se comprueba que todos los movimientos son válidos
        #  (que no choque con paredes, etc.)

        # Los Sprites que no se mueven no hace falta actualizarlos,
        #  si se actualiza el scroll, sus posiciones en pantalla se actualizan más abajo
        # En cambio, sí haría falta actualizar los Sprites que no se mueven pero que tienen que
        #  mostrar alguna animación

        # Comprobamos si hay colision entre algun jugador y algun enemigo
        # Se comprueba la colision entre ambos grupos
        # Si la hay, indicamos que se ha finalizado la fase
        #if pygame.sprite.groupcollide(self.grupoJugadores, self.grupoEnemigos, False, False)!={}:
            # Se le dice al director que salga de esta escena y ejecute la siguiente en la pila
            #self.director.salirEscena()
        print('Por implementar')
        # Actualizamos el scroll
  #      self.actualizarScroll(self.jugador1, self.jugador2)
  
        # Actualizamos el fondo:
        #  la posicion del sol y el color del cielo
        self.fondo.update(tiempo)

        
    def dibujar(self, pantalla):
        # Ponemos primero el fondo
        self.fondo.dibujar(pantalla)
        # Despues, las animaciones que haya detras
 #       for animacion in self.animacionesDetras:
  #          animacion.dibujar(pantalla)
        # Después el decorado
        self.decorado.dibujar(pantalla)
        # Luego los Sprites
  #      self.grupoSprites.draw(pantalla)
        # Y por ultimo, dibujamos las animaciones por encima del decorado
  #      for animacion in self.animacionesDelante:
  #          animacion.dibujar(pantalla)


    def eventos(self, lista_eventos):
        # Miramos a ver si hay algun evento de salir del programa
        for evento in lista_eventos:
            # Si se quiere salir, se le indica al director
            if evento.type == KEYDOWN: #Añadida también para salir dandole a escape
                #-------------SALIR PROGRAMA---------------------
                if evento.key == K_ESCAPE:
                    self.director.salirPrograma() 
                #-------------CAMBIAR ESCENA---------------------
                elif evento.key == K_c: #Trampa de salir de escena para cambiarla
                    self.crearFaseSiguiente()
                #--------------MENU PAUSA-------------------------
                elif evento.key == K_p: 
                    self.director.escenaPausada(self) #Informamos al director de cual es la escena pausada
                    self.director.salirEscena() #Salimos de la escena para poder entrar en el menu
                #--------------GAME_OVER-------------------------
                elif evento.key == K_g:
                    self.director.gameOver()
            if evento.type == pygame.QUIT:
                self.director.salirPrograma()

        # Indicamos la acción a realizar segun la tecla pulsada para cada jugador
        #teclasPulsadas = pygame.key.get_pressed()
        #self.jugador1.mover(teclasPulsadas, K_UP, K_DOWN, K_LEFT, K_RIGHT)
        #self.jugador2.mover(teclasPulsadas, K_w,  K_s,    K_a,    K_d)
    def crearFaseSiguiente(self):
        self.director.salirEscena()
        faseNueva = Fase(self.director,self.numFaseSiguiente)
        self.director.apilarEscena(faseNueva)

        
# -------------------------------------------------
# Clase Plataforma

#class Plataforma(pygame.sprite.Sprite):
#class Plataforma(MiSprite):
#    def __init__(self,rectangulo):
        # Primero invocamos al constructor de la clase padre
#        MiSprite.__init__(self)
        # Rectangulo con las coordenadas en pantalla que ocupara
#        self.rect = rectangulo
        # Y lo situamos de forma global en esas coordenadas
#        self.establecerPosicion((self.rect.left, self.rect.bottom))
        # En el caso particular de este juego, las plataformas no se van a ver, asi que no se carga ninguna imagen
#        self.image = pygame.Surface((0, 0))


# -------------------------------------------------
# Clase Cielo: aún no tiene nada prácticamente, solo un background negro.

class Cielo:
    def __init__(self,nombreFase):
        self.posicionx = 0 # El lado izquierdo de la subimagen que se esta visualizando
        self.update(0)

    def update(self, tiempo):
        # Calculamos el color del cielo
        self.colorCielo = (0, 0, 0)
        
    def dibujar(self,pantalla):
        # Dibujamos el color del cielo
        pantalla.fill(self.colorCielo)


# -------------------------------------------------
# Clase Decorado

class Decorado:
    def __init__(self,nombreFase):
        self.imagen = GestorRecursos.CargarImagen('Fase'+nombreFase+'\decorado.png', -1)
        self.imagen = pygame.transform.scale(self.imagen, (1200, 400))

        self.rect = self.imagen.get_rect()
        self.rect.bottom = ALTO_PANTALLA

        # La subimagen que estamos viendo
        self.rectSubimagen = pygame.Rect(0, 0, ANCHO_PANTALLA, ALTO_PANTALLA)
        self.rectSubimagen.left = 0 # El scroll horizontal empieza en la posicion 0 por defecto

    def update(self, scrollx):
        self.rectSubimagen.left = scrollx

    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, self.rect, self.rectSubimagen)
