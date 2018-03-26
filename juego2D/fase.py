# -*- coding: utf-8 -*-

import pygame
import escena
import time
from escena import *
from personajes import *
from pygame.locals import *
from constantes import *
from textoGUI import *
from objetos import *
from cielo import *
from decorado import *
from constantes import *
from careto import *
from vida import *
from tiempo import *
from elementosDibujables import *
#from animaciones import *


ULTIMA_FASE = 3
# Los bordes de la pantalla para hacer scroll horizontal
MINIMO_X_JUGADOR = 50
MAXIMO_X_JUGADOR = ANCHO_PANTALLA - MINIMO_X_JUGADOR



class Fase(Escena):
    # Crear Escenas habituales
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
        # Condicion_pasar_fase establece si inicialmente es posible pasar la fase o si no lo es.
        # Las condiciones que pueden hacer que se pasen o no de fase son: matar
        # a un enemigo o conseguir un objeto principal.

     
        self.vidaGestor = GestorRecursos.getVida() 




        # Necesito que sea string para ponerlo en la ruta.
        self.numFase = numFase
        self.numFaseSiguiente = int(numFase) + 1
        GestorRecursos.setConfiguration(self.numFase)
        self.pasarFase = GestorRecursos.getConfiguration('PASAR_FASE')

        # Primero invocamos al constructor de la clase padre
        Escena.__init__(self, director)
        #  En ese caso solo hay scroll horizontal
        self.crearElementosBordeSuperior("/" + self.numFase)

        # Creamos el decorado y el fondo
        self.decorado = Decorado("/" + self.numFase)
        self.fondo = Cielo("/" + self.numFase)
        self.elementosDibujables = ElementosDibujables()
        # Tengo dudas de que hacer con esto una vez tengamos que sea todo
        # diferente dependiendo de la fase.
        self.inventario = Inventario()

        # Aqui reunidos todos los elementos dibujables.
        self.elementosDibujables.agregarElementos(
            [self.fondo, self.decorado, self.vida, self.careto, self.tiempo, self.inventario])
        # Que parte del decorado estamos visualizando
        self.scrollx = 0

        self.determinarPlataforma()
        self.crearPlataformas(self.coordPlataforma)
        self.crearPersonajePrincipal()
        self.inicializarEnemigos()
        self.crearEnemigos()
        #self.crearEnemigos(300, self.coordPlataforma[1] +1)
        #self.crearEnemigos(500, self.coordPlataforma[1] +1)

        # Creamos un grupo con las balas.
        #self.grupoBalas = pygame.sprite.Group()
        self.grupoBalasJugador = pygame.sprite.Group()
        self.grupoBalasSoldado = pygame.sprite.Group()

        self.grupoSpritesDinamicos = pygame.sprite.Group(
            self.jugador, self.grupoEnemigos)
        # Crear objetos de momento crea la gasolina pero hay que hacerlo generico para que del
        # fichero de texto decida que es lo qeu tiene que crear y donde. Esto es tarea de Javier
        # Eduardo Penas.

        self.grupoSprites = pygame.sprite.Group(
            self.plataformaSuelo, self.grupoEnemigos)
        self.crearObjetoPrincipal()
        self.kitsCurativos = self.crearKitCurativo()
        for kitCurativo in iter(self.kitsCurativos):
            self.grupoSprites.add(kitCurativo)
        self.grupoSprites.add(self.jugador)



    def condicionesPasarFase(self):
        return self.pasarFase


    # TODO: generalizar.
    def crearPersonajePrincipal(self,):
        self.jugador = Jugador(self.vidaGestor)
        # Ponemos al jugador en la posición inicial
        self.jugador.establecerPosicion((5, self.coordPlataforma[1] + 1))


    # TODO: generalizar.
   # def crearPlataformasSecundarias():

    # TODO: generalizar
    def crearElementosBordeSuperior(self, nombreFase):
        self.careto = Careto(nombreFase)
        self.vida = listaVidas(self.vidaGestor)
        self.tiempo = Tiempo(0)

    def inicializarEnemigos(self):
        self.grupoEnemigos = pygame.sprite.Group()
        self.grupoSoldados = pygame.sprite.Group()
        self.grupoZombies = pygame.sprite.Group()


    # TODO: generalizar.
    def crearEnemigos(self):
        for (enemigo) in iter(GestorRecursos.getConfiguration('ENEMIGOS')):
            (tipoEnemigo, posicion) = enemigo
            if tipoEnemigo == 'Soldado':
                enemy = Soldado()
                self.grupoSoldados.add(enemy)
            elif tipoEnemigo == 'Zombie':
                enemy = Zombie()
                self.grupoZombies.add(enemy)
            enemy.establecerPosicion((posicion, self.coordPlataforma[1] + 1))
            self.grupoEnemigos.add(enemy)

    def crearKitCurativo(self):
        kitsCurativos = []
        for (kitCurativoConfig) in iter(GestorRecursos.getConfiguration('KIT_CURACION')):
            (vida,posicionX) = kitCurativoConfig
            kitCurativo = KitCuracion(vida)
            kitCurativo.establecerPosicion(((posicionX),self.coordPlataforma[1] + 5))
            kitsCurativos.append(kitCurativo)
        return kitsCurativos


    def determinarPlataforma(self):
        self.coordPlataforma = GestorRecursos.getConfiguration('PLATAFORMA')


    # TODO: generalizar.
    def crearPlataformas(self, coordenadas):
        self.plataformaSuelo = Plataforma(pygame.Rect(coordenadas))
        self.grupoPlataformas = pygame.sprite.Group(self.plataformaSuelo)


    # TODO: generalizar. De momento esto de generico tiene una mierda pero
    # dejemoslo asi.
    def crearObjetoPrincipal(self):
        (nombreObjetoPrincipal,posicionX,posInventario) = GestorRecursos.getConfiguration('OBJETO_PRINCIPAL')
        # En caso de existir se añade pero en caso de que no se añade nada.
        if nombreObjetoPrincipal != None:
            self.objeto = ObjetoPrincipal(
                nombreObjetoPrincipal, 'ficheroTextoQueActualmenteNoHaceNada', self.numFase)
            self.objeto.establecerPosicion((1000, self.coordPlataforma[1] + 1))
            self.grupoSprites.add(self.objeto)

<<<<<<< HEAD

    def crearKitCurativo(self):
        kitsCurativos = []
        kitCurativo = KitCuracion(50)
        kitCurativo.establecerPosicion((100, self.coordPlataforma[1] + 1))
        kitsCurativos.append(kitCurativo)
        return kitsCurativos

    
=======
>>>>>>> origin/master
    # TODO repasar los comentarios por que no corresponden de los scrolls
    def actualizarScrollOrdenados(self, jugador):

        # Si el jugador de la izquierda se encuentra más allá del borde
        # izquierdo
        if (jugador.rect.left < MINIMO_X_JUGADOR):
            desplazamiento = MINIMO_X_JUGADOR - jugador.rect.left

            # Si el escenario ya está a la izquierda del todo, no lo movemos
            # mas
            if self.scrollx <= 0:
                self.scrollx = 0

                # En su lugar, colocamos al jugador que esté más a la izquierda
                # a la izquierda de todo
                jugador.establecerPosicion(
                    (MINIMO_X_JUGADOR, jugador.posicion[1]))

                return False  # No se ha actualizado el scroll

            # Si no, es posible que el jugador de la derecha no se pueda desplazar
            # tantos pixeles a la derecha por estar muy cerca del borde derecho
            elif ((MAXIMO_X_JUGADOR - jugador.rect.right) < desplazamiento):

                # En este caso, ponemos el jugador de la izquierda en el lado
                # izquierdo
                jugador.establecerPosicion(
                    (jugador.posicion[0] + desplazamiento, jugador.posicion[1]))

                return False  # No se ha actualizado el scroll

            # Si se puede hacer scroll a la izquierda
            else:
                # Calculamos el nivel de scroll actual: el anterior - desplazamiento
                #  (desplazamos a la izquierda)
                self.scrollx = self.scrollx - desplazamiento

                return True  # Se ha actualizado el scroll

        # Si el jugador se encuentra más allá de la derecha.
        if (jugador.rect.right > MAXIMO_X_JUGADOR):

            # Se calcula cuantos pixeles esta fuera del borde
            desplazamiento = jugador.rect.right - MAXIMO_X_JUGADOR

            # Si el escenario ya está a la derecha del todo, no lo movemos mas
            if self.scrollx + ANCHO_PANTALLA >= self.decorado.rect.right:
                self.scrollx = self.decorado.rect.right - ANCHO_PANTALLA
                # En su lugar, colocamos al jugador que esté más a la derecha a
                # la derecha de todo
                jugador.establecerPosicion(
                    (self.scrollx + MAXIMO_X_JUGADOR - jugador.rect.width, jugador.posicion[1]))
                if (self.condicionesPasarFase()):  # Si se cumplen las condiciones para pasar fase

                    # Si hemos llegado a la derecha de todo creamos la escena
                    # siguiente.
                    self.director.cambiarAlMenu(self, PANTALLA_CUTSCENE)

                    return False  # No se ha actualizado el scroll

                # Si se puede hacer scroll a la derecha
            else:

                # Calculamos el nivel de scroll actual: el anterior + desplazamiento
                #  (desplazamos a la derecha)
                self.scrollx = self.scrollx + desplazamiento

                return True  # Se ha actualizado el scroll
        # Si ambos jugadores están entre los dos límites de la pantalla, no se
        # hace nada
        return False

   
    def actualizarScroll(self, jugador):
        self.actualizarScrollOrdenados(jugador)
        # Actualizamos la posición en pantalla de todos los Sprites según el
        # scroll actual
        for sprite in iter(self.grupoSprites):
            sprite.establecerPosicionPantalla((self.scrollx, 0))

        # Ademas, actualizamos el decorado para que se muestre una parte
        # distinta
        self.decorado.update(self.scrollx)

   
    def moverBalas(self, grupoBalas):
        if grupoBalas != None:
            for bala in iter(grupoBalas):
                bala.moverBala()


    def colisionEnemigoBalaAmiga(self,grupoEnemigos,tiempo):
        for enemigo in iter(grupoEnemigos):
            enemigo.mover_cpu(self.jugador, tiempo)
            for bala in self.grupoBalasJugador:
                if pygame.sprite.collide_rect(enemigo, bala):
                    self.lesionarPersonaje(bala, enemigo)
                    if not enemigo.tieneVida():
                        enemigo.kill()
            if pygame.sprite.collide_rect(self.jugador, enemigo):
                self.golpearseEnemigo(enemigo, self.jugador)

    
    def update(self, tiempo):
        # Primero, se indican las acciones que van a hacer las balas.
        self.moverBalas(self.grupoBalasJugador)
        self.moverBalas(self.grupoBalasSoldado)

        self.colisionEnemigoBalaAmiga(self.grupoSoldados,tiempo)
        self.colisionEnemigoBalaAmiga(self.grupoZombies,tiempo)

        self.cronometro = pygame.time.get_ticks() / 1000 - self.cronometroScene
        self.tiempo.actualizarCronometro(self.cronometro)
        self.fondo.update(tiempo)
        if(self.cronometro == 20):
            self.director.cambiarAlMenu(self, PANTALLA_GAMEOVER)

        self.grupoSpritesDinamicos.update(self.grupoPlataformas, tiempo)

        #--------------------- Comprobamos si hay colisión entre algún jugador
        for bala in self.grupoBalasSoldado:
            if pygame.sprite.collide_rect(self.jugador, bala):
                # Si chocan se lesiona al personaje.
                #print(self.jugador.devolverVida())
                self.lesionarPersonaje(bala, self.jugador)

        #----------------------Comprobar que el jugador esta muerto
        if not self.jugador.tieneVida():
            self.director.cambiarAlMenu(self, PANTALLA_GAMEOVER)

        #----------------------Comprobar que el jugador choca con algun kit de curacion
        for kitCurativo in self.kitsCurativos:
            if pygame.sprite.collide_rect(self.jugador, kitCurativo):
                valorKitCurativo = kitCurativo.recogerKitCurativo()
                self.jugador.recuperarVida(valorKitCurativo)
                self.vida.recuperarVida(valorKitCurativo)
                kitCurativo.vaciar()

        # ---------------------Comprobamos si hay colision entre algun jugador y el objeto principal
        if GestorRecursos.getConfiguration('OBJETO_PRINCIPAL') != (None,None,None):
            if pygame.sprite.collide_rect(self.jugador, self.objeto):
                objetoInventario = self.objeto.crearObjetoInventario(
                    int(self.numFase))
                self.inventario.guardarObjeto(objetoInventario)
                self.objeto.kill()
                self.pasarFase = True

        self.actualizarScroll(self.jugador)

    
    def lesionarPersonaje(self, bala, personaje):
        damage = bala.damageBala()
        bala.kill()
        personaje.perderVida(damage)
        if (personaje == self.jugador):
            self.vida.perderVida(damage)

    
    def golpearseEnemigo(self, enemigo, personaje):
        damage = enemigo.damageEnemigo()
        personaje.perderVida(damage)
        self.vida.perderVida(damage)

    
    def dibujar(self, pantalla):
        self.elementosDibujables.dibujar(pantalla)

        # Luego pintamos la plataforma
        self.grupoPlataformas.draw(pantalla)
        # Para pintar las balas como un sprite tienen que estar en el grupo de sprites
        # pero es el jugador quien gestiona la existencia de cada uno, por tanto, de grupoSPrites
        # En caso de existir disparos por parte del jugador se dibujan.
        self.agregarDisparosEscena(self.jugador, self.grupoBalasJugador)

        # En caso de que los enemigos tengan disparos que dar se dibujan.
        for enemigo in self.grupoSoldados:
            self.agregarDisparosEscena(enemigo, self.grupoBalasSoldado)

        # Finalmente se pinta el grupo de sprites.
        self.grupoSprites.draw(pantalla)
        # sacamos jugador y comprobamos con una variable los sprites que tiene
        # y agregamos al grupo deSprites

    
    def agregarDisparosEscena(self, pistolero, grupo):
        if (pistolero.tieneBalas()):  # Si hay balas.
            balas = pistolero.balasLanzar()
            # Su dirección va a ser hacia donde este mirando el pistolero.
            balas.mirando = pistolero.mirando
            disparo = pistolero.vaciarPistola()
            grupo.add(disparo)
            self.grupoSprites.add(disparo)
            pistolero.vaciarBalas()

    
    def eventos(self, lista_eventos):
        # Miramos a ver si hay algun evento de salir del programa
        for evento in lista_eventos:
            # Si se quiere salir, se le indica al director
            if evento.type == KEYDOWN:  # Añadida también para salir dandole a escape
                #-------------SALIR PROGRAMA---------------------
                if evento.key == K_ESCAPE:
                    self.director.salirPrograma()
                #-------------CAMBIAR ESCENA (a una cutScena)------------------
                elif evento.key == K_c:  # Trampa de salir de escena para cambiarla
                    GestorRecursos.setVida(self.jugador.devolverVida())
                    self.director.cambiarAlMenu(self, PANTALLA_CUTSCENE)
                #--------------MENU PAUSA-------------------------
                elif evento.key == K_p:
                    self.director.cambiarAlMenu(self, PANTALLA_PAUSA)
                    # self.director.salirEscena() #Salimos de la escena para
                    # poder entrar en el menu
                elif evento.key == K_v:
                    self.director.cambiarAlMenu(self, PANTALLA_VICTORIA)
                #--------------GAME_OVER-------------------------
                elif evento.key == K_g:
                    self.director.cambiarAlMenu(self, PANTALLA_GAMEOVER)
                #---------------DISPARAR--------------------------
                """elif evento.key == K_t:
		    self.jugador.dispararBala()"""
            if evento.type == pygame.QUIT:
                self.director.salirPrograma()

        teclasPulsadas = pygame.key.get_pressed()
        self.jugador.mover(teclasPulsadas, GestorRecursos.getConfigParam('teclas')['ARRIBA'],GestorRecursos.getConfigParam('teclas')['ABAJO'],
        GestorRecursos.getConfigParam('teclas')['IZQUIERDA'], GestorRecursos.getConfigParam('teclas')['DERECHA'], GestorRecursos.getConfigParam('teclas')['DISPARAR'])

    
    def teclasConfiguracion(self):
        return

   
    def obtenerNumeroFaseSiguiente(self):
        return self.numFaseSiguiente

<<<<<<< HEAD
    
    def crearSceneSiguiente(self):
        self.director.salirEscena()
        faseNueva = CutScene(self.director, self.numFaseSiguiente)
        self.director.apilarEscena(faseNueva)


=======
# -------------------------------------------------
# Clase Plataforma
class Plataforma(MiSprite):
>>>>>>> origin/master

class Plataforma(MiSprite):
    def __init__(self, rectangulo):
        # Primero invocamos al constructor de la clase padre
        MiSprite.__init__(self)
        # Rectangulo con las coordenadas en pantalla que ocupara
        self.rect = rectangulo
        # Y lo situamos de forma global en esas coordenadas
        self.establecerPosicion((self.rect.left, self.rect.bottom))
        # En el caso particular de este juego, las plataformas no se van a ver,
        # asi que no se carga ninguna imagen
        self.image = pygame.Surface((0, 0))



class CutScene(Escena):
    def __init__(self, director, numFase):
        Escena.__init__(self, director)
        # Necesito que sea string para ponerlo en la ruta.
        self.numFase = str(numFase)
        # self.numFaseSiguiente = numFase+1 #Para saber el numero de la fase siguiente
        # Primero invocamos al constructor de la clase padr

        # Creamos el decorado y el fondo
        self.fondoCutScene = FondoCutScene("/" + self.numFase)
        self.texto = TITULO
        # Velocidad a la que ira el texto de titulo.
        self.movimientoPosicion = 2


    def eventos(self, lista_eventos):
        # Miramos a ver si hay algun evento de salir del programa
        for evento in lista_eventos:
            # Si se quiere salir, se le indica al director
            if evento.type == KEYDOWN:  # Añadida también para salir dandole a escape
                #-------------SALIR PROGRAMA---------------------
                if evento.key == K_ESCAPE:
                    self.director.salirPrograma()
                #-------------CAMBIAR ESCENA ---------------------
                elif evento.key == K_RETURN:  # Trampa de salir de escena para cambiarla
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
        faseNueva = Fase(self.director, self.numFase)
        faseNueva.cronometroScene = pygame.time.get_ticks() / 1000
        self.director.apilarEscena(faseNueva)


    def actualizarTextoTituloNivel(self):
        # Actualizar el texto que corresponda.
        (posicion, _) = self.fondoCutScene.update(
            self.movimientoPosicion, self.texto)
        if posicion > 400:  # Cuando llega más o menos a la mitad del texto el titulo...:
            self.mostrarTexto()  # Se muestra el otro texto.
            self.movimientoPosicion = 1  # Se baja la velocidad


    # Dependiendo de cual de estas funciones sean se muestra el texto texto o
    # texto de titulo.
    def mostrarTexto(self):
        self.texto = TEXTO

    def mostrarTitulo(self):
        self.texto = TITULO



class FondoCutScene:
    def __init__(self, nombreFase):
        self.imagen = GestorRecursos.CargarImagen(
            'Cutscene' + nombreFase + '/Nivel.jpg', 1)
        self.imagen = pygame.transform.scale(
            self.imagen, (ANCHO_PANTALLA, ALTO_PANTALLA))
        self.textoTitulo = TextoTituloNivel(self, nombreFase)

        self.textoNivel = []

        # Leer texto, separado por líneas.
        textoLargo = self.leerArchivo(nombreFase)
        # Espacio para que empiece la primera coordenada del texto.
        coordenada = -(len(textoLargo) - 1) * 70
        for linea in textoLargo:  # Ir leyendo línea a línea.
            # Creo una nueva clase de textoNivel con coordenadas
            self.textoNivel.append(TextoNivel(self, linea, coordenada))
            coordenada += 70  # Separación entre líneas.

        self.texto = TITULO
        self.tiempoCutScene = pygame.time.get_ticks() / 1000


    def leerArchivo(self, nombreFase):
        datos = GestorRecursos.CargarArchivoCoordenadas(
            'Cutscene' + nombreFase + '/Texto.txt')
        datos = datos.splitlines()
        return datos[::-1]  # Hacerla reverse porque se lee del reves.


    def update(self, movimientoPosicion, texto):
        self.texto = texto
        if self.texto == TITULO:
            return self.textoTitulo.moverPosicion(x=movimientoPosicion)
        elif self.texto == TEXTO:
            for lineaTextoNivel in self.textoNivel:
                lineaTextoNivel.moverPosicion(y=movimientoPosicion)
            return (0, 0)

    def dibujar(self, pantalla):
        # Dibujamos primero la imagen de fondo
        pantalla.blit(self.imagen, self.imagen.get_rect())
        # if self.texto == TITULO:
        # self.textoTitulo.dibujar(pantalla)                      yo esto lo
        # quitaría porque se ve el nombre del fichero
        if self.texto == TEXTO:
            for lineaTextoNivel in self.textoNivel:
                lineaTextoNivel.dibujar(pantalla)



class TextoTituloNivel(TextoGUI):
    def __init__(self, pantalla, nombreFase):
        # La fuente la debería cargar el estor de recursos
        fuente = pygame.font.SysFont('impact', 50)
        TextoGUI.__init__(self, pantalla, fuente, BLANCO,
                          'Nivel ' + nombreFase, (100, 250))


class TextoNivel(TextoGUI):
    def __init__(self, pantalla, nombreFase, coordenada):
        fuente = pygame.font.SysFont('impact', 30)
        TextoGUI.__init__(self, pantalla, fuente, BLANCO,
                          nombreFase, (40, coordenada))
