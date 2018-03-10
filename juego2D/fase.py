# -*- coding: utf-8 -*-

import pygame, escena
from escena import *
from personajes import *
from pygame.locals import *
#from animaciones import *
from CutScene import *
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
    #Crear Escenas habituales
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

        self.numFase = numFase #Necesito que sea string para ponerlo en la ruta. 
        self.numFaseSiguiente = int(numFase)+1
        
        # Primero invocamos al constructor de la clase padre
        Escena.__init__(self, director)

        # Creamos el decorado y el fondo
        self.decorado = Decorado("/"+self.numFase)
        self.fondo = Cielo("/"+self.numFase)

        # Que parte del decorado estamos visualizando
        self.scrollx = 0
        #  En ese caso solo hay scroll horizontal
   
    def update(self, tiempo):
        #  la posicion del sol y el color del cielo
            self.fondo.update(tiempo)

        
    def dibujar(self, pantalla):
        # Ponemos primero el fondo
            self.fondo.dibujar(pantalla)
            self.decorado.dibujar(pantalla)   

    def eventos(self, lista_eventos):
        # Miramos a ver si hay algun evento de salir del programa
        for evento in lista_eventos:
            # Si se quiere salir, se le indica al director
            if evento.type == KEYDOWN: #Añadida también para salir dandole a escape
                #-------------SALIR PROGRAMA---------------------
                if evento.key == K_ESCAPE:
                    self.director.salirPrograma() 
                #-------------CAMBIAR ESCENA (a una cutScena)---------------------
                elif evento.key == K_c: #Trampa de salir de escena para cambiarla
                    self.crearSceneSiguiente()              
                #--------------MENU PAUSA-------------------------
                elif evento.key == K_p: 
                    self.director.escenaPausada(self) #Informamos al director de cual es la escena pausada
                    self.director.salirEscena() #Salimos de la escena para poder entrar en el menu
                #--------------GAME_OVER-------------------------
                elif evento.key == K_g:
                    self.director.gameOver()
            if evento.type == pygame.QUIT:
                self.director.salirPrograma()
    
    def crearSceneSiguiente(self):
        self.director.salirEscena()
        faseNueva = CutScene(self.director,self.numFaseSiguiente)
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
        
   
        
class CutScene(Escena):
    #Crear cutScenas
    def __init__(self, director, numFase):
        Escena.__init__(self, director)
        #NumFase
        self.numFase = str(numFase) #Necesito que sea string para ponerlo en la ruta.
        # self.numFaseSiguiente = numFase+1 #Para saber el numero de la fase siguiente         
        # Primero invocamos al constructor de la clase padr
    
        # Creamos el decorado y el fondo
        self.fondoCutScene = FondoCutScene("/"+self.numFase)     
    
    def eventos(self, lista_eventos):
        # Miramos a ver si hay algun evento de salir del programa
        for evento in lista_eventos:
            # Si se quiere salir, se le indica al director
            if evento.type == KEYDOWN: #Añadida también para salir dandole a escape
                #-------------SALIR PROGRAMA---------------------
                if evento.key == K_ESCAPE:
                    self.director.salirPrograma() 
                #-------------CAMBIAR ESCENA ---------------------
                elif evento.key == K_RETURN: #Trampa de salir de escena para cambiarla
                    self.crearSceneSiguiente()                
            if evento.type == pygame.QUIT:
                self.director.salirPrograma()    
                
    def update(self, tiempo):
        print('Sin implementar')
    
    def dibujar(self, pantalla):
        # Ponemos primero el fondo
        self.fondoCutScene.dibujar(pantalla) 
    
    def crearSceneSiguiente(self):
        self.director.salirEscena()
        faseNueva = Fase(self.director,self.numFase)
        self.director.apilarEscena(faseNueva)        
        
        
class FondoCutScene:
    def __init__(self,nombreFase):
        self.imagen = GestorRecursos.CargarImagen('Cutscene'+nombreFase+'/Nivel.jpg', 1)
        self.imagen = pygame.transform.scale(self.imagen, (ANCHO_PANTALLA, ALTO_PANTALLA))
    
    def update(self, scrollx):
        print("No hace nada update")
        #self.rectSubimagen.left = scrollx

    def dibujar(self, pantalla):
        #Dibujamos primero la imagen de fondo
        pantalla.blit(self.imagen, self.imagen.get_rect())   
    
