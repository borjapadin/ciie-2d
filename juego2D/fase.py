# -*- coding: utf-8 -*-

import pygame, escena, time
from escena import *
from personajes import *
from pygame.locals import *
from constantes import *
from textoGUI import *
from objetos import *
from Cielo import *
from decorado import *
from constantes import *
from careto import *
from vida import *
from Tiempo import *
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
    	self.pasarFase = False
        self.numFase = numFase #Necesito que sea string para ponerlo en la ruta.
        self.numFaseSiguiente = int(numFase)+1

        # Primero invocamos al constructor de la clase padre
        Escena.__init__(self, director)
	   #  En ese caso solo hay scroll horizontal
        self.crearElementosBordeSuperior("/"+self.numFase)
	
        # Creamos el decorado y el fondo
        self.decorado = Decorado("/"+self.numFase)
        self.fondo = Cielo("/"+self.numFase)

        # Que parte del decorado estamos visualizando
        self.scrollx = 0

    	self.crearPlataformas()
    	self.crearPersonajePrincipal()
        self.inicializarEnemigos()
    	self.crearEnemigos(300, 401)
        self.crearEnemigos(500, 401)
        self.crearObjetoPrincipal()

	   # Creamos un grupo con las balas.
        #self.grupoBalas = pygame.sprite.Group()
        self.grupoBalasJugador = pygame.sprite.Group()
        self.grupoBalasSoldado = pygame.sprite.Group()
	

        self.grupoSpritesDinamicos = pygame.sprite.Group(self.jugador, self.grupoEnemigos)
    	#Crear objetos de momento crea la gasolina pero hay que hacerlo generico para que del
    	#fichero de texto decida que es lo qeu tiene que crear y donde. Esto es tarea de Javier
    	#Eduardo Penas.
    	
        self.grupoSprites = pygame.sprite.Group(self.jugador,self.plataformaSuelo,self.objeto, self.grupoEnemigos)
    def condicionesPasarFase(self):
	return self.pasarFase
    
    #TODO: generalizar.
    def crearPersonajePrincipal(self):
    	self.jugador = Jugador()
    	#Ponemos al jugador en la posición inicial
    	self.jugador.establecerPosicion((5, 401))
   
    #TODO: generalizar.
   # def crearPlataformasSecundarias():
    
    #TODO: generalizar
    def crearElementosBordeSuperior(self,nombreFase):
    	self.careto = Careto(nombreFase)
    	self.vida = listaVidas()
    	self.tiempo = Tiempo((0,0))

    def inicializarEnemigos(self):
        self.grupoEnemigos = pygame.sprite.Group()
	
    #TODO: generalizar.
    def crearEnemigos(self, x, y):
    	enemigo = Soldado()
    	enemigo.establecerPosicion((x,y))
    	self.grupoEnemigos.add(enemigo)	
    
    #TODO: generalizar.
    def crearPlataformas(self):
    	self.plataformaSuelo = Plataforma(pygame.Rect(0, 400, 1200, 15))
    	self.grupoPlataformas = pygame.sprite.Group(self.plataformaSuelo)	
    
    #TODO: generalizar. De momento esto de generico tiene una mierda pero dejemoslo asi.
    def crearObjetoPrincipal(self):
    	self.objeto = BidonGasolina()
    	self.objeto.establecerPosicion((1000,401))

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
    		if (self.condicionesPasarFase()): #Si se cumplen las condiciones para pasar fase

    		    # Si hemos llegado a la derecha de todo creamos la escena siguiente.
    		    self.director.cambiarAlMenu(self,PANTALLA_CUTSCENE)

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
        # Primero, se indican las acciones que van a hacer las balas.
        if self.grupoBalasJugador != None or self.grupoBalasSoldado != None:
            for bala in iter(self.grupoBalasJugador):
                bala.moverBala()
            for bala in iter(self.grupoBalasSoldado):
                bala.moverBala()

        for enemigo in iter(self.grupoEnemigos): #************************* LEEER COMENTARIO DE ABAJO
            enemigo.mover_cpu_distancia(self.jugador,tiempo)
            for bala in self.grupoBalasJugador:
                if pygame.sprite.collide_rect(enemigo, bala):
                    damage = bala.damageBala()
                    bala.kill()
                    enemigo.perderVida(damage)
                    if not enemigo.tieneVida():
                        enemigo.kill()

        self.fondo.update(tiempo)
        self.grupoSpritesDinamicos.update(self.grupoPlataformas, tiempo)
	
    	#------------------- Comprobamos si hay colisión entre algún jugador y una bala enemiga ----------
    	for bala in self.grupoBalasSoldado:
    	    if pygame.sprite.collide_rect(self.jugador, bala):
    		damage = bala.damageBala()
    		bala.kill()
    		#Esta situacion no me agrada: el jugador pierde vida no esta directamente relacionado con la vida que se muestra en pantalla mmm...
    		self.jugador.perderVida(25)
    		self.vida.perderVida(damage) #De momento pierde vida 25 porque me da pereza otra cosa
    	#------------------- En principio he dejado estas dos partes separadas porque no estoy muy segura de como hacerlas ---
    	# Podriamos decir que el soldado enemigo sufre el fuego amigo (de sus compañeros) entonces quedaria igual.... pero no veo yo muy viable
    	# Hacer esto... así que habria que modificar varias cosas. Además de que si no hacemos fuego enemigo para los amigos tampoco deberíamos
    	# para el prota (porque va a resultar más natural programarlo asi), de todas maneras tampoco creo que se pudiera dar esa situacion
    	# si la bala es lo suficiente rápida.
    	
    	if not self.jugador.tieneVida():
    	    self.director.cambiarAlMenu(self,PANTALLA_GAMEOVER)
	
	
        # Comprobamos si hay colision entre algun jugador y el objeto principal
    	if pygame.sprite.collide_rect(self.jugador, self.objeto):
    	    self.objeto.kill()
    	    self.pasarFase = True
	

        self.actualizarScroll(self.jugador)

    def dibujar(self, pantalla):
        # Ponemos primero el fondo
        self.fondo.dibujar(pantalla)
        # Luego el decorado.
        self.decorado.dibujar(pantalla)
        # Dibujamos el menu
    	self.careto.dibujar(pantalla)
    	self.vida.dibujar(pantalla)
    	self.tiempo.dibujar(pantalla)
	
        # Luego pintamos la plataforma
        self.grupoPlataformas.draw(pantalla)
        # Para pintar las balas como un sprite tienen que estar en el grupo de sprites
        # pero es el jugador quien gestiona la existencia de cada uno, por tanto, de grupoSPrites
        #En caso de existir disparos por parte del jugador se dibujan.
        self.agregarDisparosEscena(self.jugador,self.grupoBalasJugador)
	
        #En caso de que los enemigos tengan disparos que dar se dibujan.
    	for enemigo in self.grupoEnemigos:
    	    self.agregarDisparosEscena(enemigo,self.grupoBalasSoldado)

        # Finalmente se pinta el grupo de sprites.
    	self.grupoSprites.draw(pantalla)
        # sacamos jugador y comprobamos con una variable los sprites que tiene y agregamos al grupo deSprites
    
    def agregarDisparosEscena(self,pistolero,grupo):
        if (pistolero.tieneBalas()): #Si hay balas.
    	    balas = pistolero.balasLanzar()
    	    balas.mirando = pistolero.mirando #Su dirección va a ser hacia donde este mirando el pistolero.
    	    disparo = pistolero.vaciarPistola()
    	    grupo.add(disparo)
    	    self.grupoSprites.add(disparo)
    	    pistolero.vaciarBalas()
	    
	    
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
                    self.director.cambiarAlMenu(self,PANTALLA_CUTSCENE)
                #--------------MENU PAUSA-------------------------
                elif evento.key == K_p:
                    self.director.cambiarAlMenu(self,PANTALLA_PAUSA)
                    #self.director.salirEscena() #Salimos de la escena para poder entrar en el menu
		elif evento.key == K_v:
		    self.director.cambiarAlMenu(self,PANTALLA_VICTORIA)
                #--------------GAME_OVER-------------------------
                elif evento.key == K_g:
                    self.director.cambiarAlMenu(self,PANTALLA_GAMEOVER)
		#---------------DISPARAR--------------------------
		"""elif evento.key == K_t:
		    self.jugador.dispararBala()"""
            if evento.type == pygame.QUIT:
                self.director.salirPrograma()

        teclasPulsadas = pygame.key.get_pressed()
        self.jugador.mover(teclasPulsadas, K_w, K_s, K_a, K_d, K_t)

    def obtenerNumeroFaseSiguiente(self):
    	return self.numFaseSiguiente

    def crearSceneSiguiente(self):
        self.director.salirEscena()
        faseNueva = CutScene(self.director,self.numFaseSiguiente)
        self.director.apilarEscena(faseNueva)

# -------------------------------------------------
# Clase Plataforma
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
