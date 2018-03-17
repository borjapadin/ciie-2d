# -*- coding: utf-8 -*-

import pygame, escena
from escena import *
from personajes import *
from pygame.locals import *
from Constantes import *
from TextoGUI import *
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

        plataformaSuelo = Plataforma(pygame.Rect(0, 400, 1200, 15))

        self.grupoPlataformas = pygame.sprite.Group( plataformaSuelo)
        #iniciamos el jugador
        self.jugador = Jugador()
        #Ponemos al jugador en la posición inicial
        self.jugador.establecerPosicion((5, 401))

        self.grupoSpritesDinamicos = pygame.sprite.Group( self.jugador)
	
        self.grupoSprites = pygame.sprite.Group(self.jugador,plataformaSuelo)

#TODO repasar los comentarios por que no corresponden de los scrolls
    def actualizarScrollOrdenados(self, jugador):

        # Si el jugador de la izquierda se encuentra más allá del borde izquierdo
        if (jugador.rect.left<MINIMO_X_JUGADOR):
            desplazamiento = MINIMO_X_JUGADOR - jugador.rect.left

            # Si el escenario ya está a la izquierda del todo, no lo movemos mas
            if self.scrollx <= 0:
                self.scrollx = 0

                # En su lugar, colocamos al jugador que esté más a la izquierda a la izquierda de todo
                jugador.establecerPosicion((MINIMO_X_JUGADOR, jugador.posicion[1]))

                return False; # No se ha actualizado el scroll

            # Si no, es posible que el jugador de la derecha no se pueda desplazar
            #  tantos pixeles a la derecha por estar muy cerca del borde derecho
            elif ((MAXIMO_X_JUGADOR-jugador.rect.right)<desplazamiento):

                # En este caso, ponemos el jugador de la izquierda en el lado izquierdo
                jugador.establecerPosicion((jugador.posicion[0]+desplazamiento, jugador.posicion[1]))

                return False; # No se ha actualizado el scroll


            # Si se puede hacer scroll a la izquierda
            else:
                # Calculamos el nivel de scroll actual: el anterior - desplazamiento
                #  (desplazamos a la izquierda)
                self.scrollx = self.scrollx - desplazamiento;

                return True; # Se ha actualizado el scroll
	
	#Si el jugador se encuentra más allá de la derecha.
        if (jugador.rect.right>MAXIMO_X_JUGADOR):

            # Se calcula cuantos pixeles esta fuera del borde
            desplazamiento = jugador.rect.right - MAXIMO_X_JUGADOR

            # Si el escenario ya está a la derecha del todo, no lo movemos mas
            if self.scrollx + ANCHO_PANTALLA >= self.decorado.rect.right:
                self.scrollx = self.decorado.rect.right - ANCHO_PANTALLA

                # En su lugar, colocamos al jugador que esté más a la derecha a la derecha de todo
                jugador.establecerPosicion((self.scrollx+MAXIMO_X_JUGADOR-jugador.rect.width, jugador.posicion[1]))
		# Si hemos llegado a la derecha de todo creamos la escena siguiente.
		self.crearSceneSiguiente()
                return False; # No se ha actualizado el scroll

            # Si se puede hacer scroll a la derecha
            else:

                # Calculamos el nivel de scroll actual: el anterior + desplazamiento
                #  (desplazamos a la derecha)
                self.scrollx = self.scrollx + desplazamiento;

                return True; # Se ha actualizado el scroll
        # Si ambos jugadores están entre los dos límites de la pantalla, no se hace nada
        return False;


    def actualizarScroll(self, jugador):
        self.actualizarScrollOrdenados(jugador)
        # Actualizamos la posición en pantalla de todos los Sprites según el scroll actual
        for sprite in iter(self.grupoSprites):
            sprite.establecerPosicionPantalla((self.scrollx, 0))

        # Ademas, actualizamos el decorado para que se muestre una parte distinta
        self.decorado.update(self.scrollx)


    def update(self, tiempo):
        self.fondo.update(tiempo)
        self.grupoSpritesDinamicos.update(self.grupoPlataformas, tiempo)
        self.actualizarScroll(self.jugador)
        #TODO detectar que se acabo la fase y cambiarla

    def dibujar(self, pantalla):
        # Ponemos primero el fondo
        self.fondo.dibujar(pantalla)
	# Luego el decorado.
        self.decorado.dibujar(pantalla)
	# Luego pintamos la plataforma
        self.grupoPlataformas.draw(pantalla)
	# Para pintar las balas como un sprite tienen que estar en el grupo de sprites
	# pero es el jugador quien gestiona la existencia de cada uno, por tanto, de grupoSPrites
	# sacamos jugador y comprobamos con una variable los sprites que tiene y agregamos al grupo deSprites
	balas = self.jugador.balasLanzar() 
	if balas != None:	        
	    self.grupoSprites.add(balas) #Se agrega la bala a los sprites del juego.

	# Finalmente se pinta el grupo de sprites.
	self.grupoSprites.draw(pantalla)	

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
                    self.director.cambiarAlMenu(self,PANTALLA_PAUSA)
                    #self.director.salirEscena() #Salimos de la escena para poder entrar en el menu
		elif evento.key == K_v:
		    self.director.cambiarAlMenu(self,PANTALLA_VICTORIA)
                #--------------GAME_OVER-------------------------
                elif evento.key == K_g:
                    self.director.cambiarAlMenu(self,PANTALLA_GAMEOVER)
            if evento.type == pygame.QUIT:
                self.director.salirPrograma()

        teclasPulsadas = pygame.key.get_pressed()
        self.jugador.mover(teclasPulsadas, K_w, K_s, K_a, K_d, K_t)

    def crearSceneSiguiente(self):
        self.director.salirEscena()
        faseNueva = CutScene(self.director,self.numFaseSiguiente)
        self.director.apilarEscena(faseNueva)

# -------------------------------------------------
# Clase Plataforma

#class Plataforma(pygame.sprite.Sprite):
class Plataforma(MiSprite):
    def __init__(self,rectangulo):
        # Primero invocamos al constructor de la clase padre
        MiSprite.__init__(self)
        # Rectangulo con las coordenadas en pantalla que ocupara
        self.rect = rectangulo
        # Y lo situamos de forma global en esas coordenadas
        self.establecerPosicion((self.rect.left, self.rect.bottom))
        # En el caso particular de este juego, las plataformas no se van a ver, asi que no se carga ninguna imagen
        self.image = pygame.Surface((0, 0))



# -------------------------------------------------
# Clase Cielo: aún no tiene nada prácticamente, solo un background negro.

class Cielo:
    def __init__(self,nombreFase):
        self.posicionx = 0 # El lado izquierdo de la subimagen que se esta visualizando
        self.update(0)

    def update(self, tiempo):
        # Calculamos el color del cielo
        self.colorCielo = NEGRO

    def dibujar(self,pantalla):
        # Dibujamos el color del cielo
        pantalla.fill(self.colorCielo)
        self.colorCielo = NEGRO


# -------------------------------------------------
# Clase Decorado

class Decorado:
    def __init__(self,nombreFase):
        self.imagen = GestorRecursos.CargarImagen('Fase'+nombreFase+'/decorado.png', -1)
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
        self.texto = TITULO
        self.movimientoPosicion = 2 #Velocidad a la que ira el texto de titulo.

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
        self.actualizarTextoTituloNivel()

    def dibujar(self, pantalla):
        # Ponemos primero el fondo
        self.fondoCutScene.dibujar(pantalla)

    def crearSceneSiguiente(self):
        self.director.salirEscena()
        faseNueva = Fase(self.director,self.numFase)
        self.director.apilarEscena(faseNueva)

    def actualizarTextoTituloNivel(self):


        (posicion,_) = self.fondoCutScene.update(self.movimientoPosicion,self.texto) #Actualizar el texto que corresponda.
        if posicion > 400: #Cuando llega más o menos a la mitad del texto el titulo...:
            self.mostrarTexto() #Se muestra el otro texto.
            self.movimientoPosicion = 1 #Se baja la velocidad

    #Dependiendo de cual de estas funciones sean se muestra el texto texto o texto de titulo.
    def mostrarTexto(self):
        self.texto = TEXTO

    def mostrarTitulo(self):
        self.texto = TITULO


class FondoCutScene:
    def __init__(self,nombreFase):
        self.imagen = GestorRecursos.CargarImagen('Cutscene'+nombreFase+'/Nivel.jpg', 1)
        self.imagen = pygame.transform.scale(self.imagen, (ANCHO_PANTALLA, ALTO_PANTALLA))
        self.textoTitulo = TextoTituloNivel(self,nombreFase)

        self.textoNivel = []

        textoLargo = self.leerArchivo(nombreFase) #Leer texto, separado por líneas.
        coordenada = -(len(textoLargo)-1)*70 #Espacio para que empiece la primera coordenada del texto.
        for linea in textoLargo: #Ir leyendo línea a línea.
            self.textoNivel.append(TextoNivel(self,linea,coordenada)) #Creo una nueva clase de textoNivel con coordenadas
            coordenada += 70 #Separación entre líneas.


        self.texto = TITULO

    def leerArchivo(self,nombreFase):
	print (type (nombreFase))
        datos = GestorRecursos.CargarArchivoCoordenadas('Cutscene'+nombreFase+'/Texto.txt')
        datos = datos.splitlines()
        return datos[::-1] #Hacerla reverse porque se lee del reves.

    def update(self,movimientoPosicion,texto):
        self.texto = texto
        if self.texto == TITULO:
            return self.textoTitulo.moverPosicion(x=movimientoPosicion)
        elif self.texto == TEXTO:
            for lineaTextoNivel in self.textoNivel:
                lineaTextoNivel.moverPosicion(y=movimientoPosicion)
            return (0,0)

    def dibujar(self, pantalla):
        #Dibujamos primero la imagen de fondo
        pantalla.blit(self.imagen, self.imagen.get_rect())
        #if self.texto == TITULO:
        #    self.textoTitulo.dibujar(pantalla)    			yo esto lo quitaría porque se ve el nombre del fichero
        if self.texto == TEXTO:
            for lineaTextoNivel in self.textoNivel:
                lineaTextoNivel.dibujar(pantalla)

class TextoTituloNivel(TextoGUI):
    def __init__(self, pantalla, nombreFase):
        # La fuente la debería cargar el estor de recursos
        fuente = pygame.font.SysFont('impact', 50);
        TextoGUI.__init__(self, pantalla, fuente, BLANCO, 'Nivel '+nombreFase, (100, 250))

class TextoNivel(TextoGUI):
    def __init__(self, pantalla, nombreFase, coordenada):
        fuente = pygame.font.SysFont('impact', 30);
        TextoGUI.__init__(self, pantalla, fuente, BLANCO, nombreFase, (40, coordenada))
