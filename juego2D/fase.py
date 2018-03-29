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
from plataforma import *
from loggerCreator import *

ULTIMA_FASE = 3
# Los bordes de la pantalla para hacer scroll horizontal
MINIMO_X_JUGADOR = 50
MAXIMO_X_JUGADOR = ANCHO_PANTALLA - MINIMO_X_JUGADOR



class Fase(Escena):
    # Crear Escenas habituales
    def __init__(self, director, numFase, cronometroScene):
        self.cronometroScene = cronometroScene
        self.tiempoAntesDePausa = 0
        self.tiempoEnPausa = 0
        self.logger = loggerCreator.getLogger('loger','loger.log')
        self.vidaGestor = GestorRecursos.getVida()
        # Necesito que sea string para ponerlo en la ruta.
        self.numFase = numFase
        self.numFaseSiguiente = int(numFase) + 1
        # El gestor de recursos cargara todos los recursos a partir de ese numero.
        self.pasarFase = GestorRecursos.getConfiguration('PASAR_FASE')
        self.tiempoFase = GestorRecursos.getConfiguration(
            'TIEMPO') + GestorRecursos.getTiempoAcumulado()

        # Primero invocamos al constructor de la clase padre
        Escena.__init__(self, director)
        #  En ese caso solo hay scroll horizontal
        self.crearElementosBordeSuperior("/" + self.numFase)

        # Creamos el decorado y el fondo
        self.decorado = Decorado("/" + self.numFase, GestorRecursos.getConfiguration('POSICION_DECORADO'))
        self.fondo = Cielo("/" + self.numFase)
        self.elementosDibujables = ElementosDibujables()
        self.inventario = Inventario(GestorRecursos.getInventario())

        # Aqui reunidos todos los elementos dibujables.
        self.elementosDibujables.agregarElementos(
            [self.fondo, self.decorado, self.vida, self.careto, self.tiempo, self.inventario])
        # Si tiene boss entonces pintamos su vida y su jepeto
        if (GestorRecursos.getConfiguration('TIENE_BOSS')):
            self.listaVidasEnemigo = listaVidasEnemigo()
            self.elementosDibujables.agregarElemento(self.listaVidasEnemigo)
        # Que parte del decorado estamos visualizando
        self.scrollx = 0

        self.determinarPlataforma()
        if GestorRecursos.getConfiguration('TIENE_BARCO') == True:
            self.barco = pygame.sprite.Group()
            self.crearBarco()
        self.crearPlataformas(self.coordPlataforma)
        self.crearPersonajePrincipal()
        self.inicializarEnemigos()
        self.crearEnemigos()

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
            self.grupoPlataformas,self.grupoEnemigos)
        self .grupoObjetos = pygame.sprite.Group()
        if self.numFase == 2:
            self.grupoSPrites.add(self.barco)

        self.crearObjetoPrincipal()
        #Crear kits curativos
        self.kitsCurativos = self.crearKitCurativo()
        for kitCurativo in iter(self.kitsCurativos):
            self.grupoSprites.add(kitCurativo)
            self.grupoObjetos.add(kitCurativo)
        self.grupoSprites.add(self.jugador)

        self.cronometro = pygame.time.get_ticks() / 1000 - self.cronometroScene

    def condicionesPasarFase(self):
        return self.pasarFase


    # TODO: generalizar.
    def crearPersonajePrincipal(self,):
        self.grupoJugador = pygame.sprite.Group()
        self.jugador = Jugador(self.vidaGestor)
        self.grupoJugador.add(self.jugador)
        # Ponemos al jugador en la posición inicial
        self.jugador.establecerPosicion((5, self.coordPlataforma[1] + 1))

    # TODO: generalizar
    def crearElementosBordeSuperior(self, nombreFase):
        self.careto = Careto(nombreFase)
        self.vida = listaVidas(self.vidaGestor)
        self.tiempo = Tiempo(self.tiempoFase)

    def inicializarEnemigos(self):
        self.grupoEnemigos = pygame.sprite.Group()
        self.grupoSoldados = pygame.sprite.Group()
        self.grupoZombies = pygame.sprite.Group()

    def crearPlataformasSecundarias(self):
        plataformasSecundarias = []
        for (datosPlataforma) in iter(GestorRecursos.getConfiguration('PLATAFORMA_SECUNDARIA')):
            (imagen,posicionX,posicionY) = datosPlataforma
            plataformaSecundaria = PlataformaSecundaria(imagen)
            plataformaSecundaria.establecerPosicion((posicionX,posicionY))
            plataformasSecundarias.append(plataformaSecundaria)
        return plataformasSecundarias

    def crearBarco(self):
        
        for (datosBarco) in iter(GestorRecursos.getConfiguration('BARCO')):
            (imagen,posicionX,posicionY) = datosBarco
            barcoTemp = Barco(imagen)
            barcoTemp.establecerPosicion((posicionX,posicionY))
            self.barco.add(barcoTemp)

    # TODO: generalizar.
    def crearEnemigos(self):
        for (enemigo) in iter(GestorRecursos.getConfiguration('ENEMIGOS')):
            (tipoEnemigo, posicion) = enemigo
            if tipoEnemigo == 'Soldado':
                enemy = Soldado()
                self.grupoSoldados.add(enemy)
            if tipoEnemigo == 'Boss':
                enemy = Boss()
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
        self.grupoPlataformas = pygame.sprite.Group()
        self.plataformaSuelo = Plataforma(pygame.Rect(coordenadas))

        #Crear plataformas secundarias
        self.plataformasSecundarias = self.crearPlataformasSecundarias()
        # Recorrerlas y meterlas en el grupo de plataformas.
        for plataformaSecundaria in iter(self.plataformasSecundarias):
            self.grupoPlataformas.add(plataformaSecundaria)
        self.grupoPlataformas.add(self.plataformaSuelo)
        if GestorRecursos.getConfiguration('TIENE_BARCO') == True:
            self.grupoPlataformas.add(self.barco)



    # TODO: generalizar. De momento esto de generico tiene una mierda pero
    # dejemoslo asi.
    def crearObjetoPrincipal(self):
        if (GestorRecursos.getConfiguration('TIENE_OBJETO_PRINCIPAL')):
            posicionX = GestorRecursos.getConfiguration('COORDENADAS_OBJETO_PRINCIPAL')
            nombreObjetoPrincipal = GestorRecursos.getConfiguration('IMAGEN_OBJETO_PRINCIPAL')
            posicionObjetoPrincipalInventario = GestorRecursos.getConfiguration('POSICION_OBJETO_PRINCIPAL')
            # En caso de existir se añade pero en caso de que no se añade nada.
            if nombreObjetoPrincipal != None:
                self.objeto = ObjetoPrincipal(
                    nombreObjetoPrincipal, int(posicionObjetoPrincipalInventario))
                self.objeto.establecerPosicion((1000, self.coordPlataforma[1] + 1))
                self.grupoSprites.add(self.objeto)
                self.grupoObjetos.add(self.objeto)

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
        if (jugador.rect.right > MAXIMO_X_JUGADOR/2):

            # Se calcula cuantos pixeles esta fuera del borde
            desplazamiento = jugador.rect.right - MAXIMO_X_JUGADOR/2

            # Si el escenario ya está a la derecha del todo, no lo movemos mas
            if self.scrollx + ANCHO_PANTALLA >= self.decorado.rect.right:
                self.scrollx = self.decorado.rect.right - ANCHO_PANTALLA
                
                if (jugador.rect.right > MAXIMO_X_JUGADOR):
                    jugador.establecerPosicion((self.scrollx + MAXIMO_X_JUGADOR - jugador.rect.width, jugador.posicion[1]))

                    if (self.condicionesPasarFase()):  # Si se cumplen las condiciones para pasar fase

                        # Si hemos llegado a la derecha de todo creamos la escena
                        # siguiente, además de que reseteamos la vida.
                        if GestorRecursos.getConfiguration('TIENE_BOSS') != True:
                            # ESTO TIENE QUE IR PAH UNA FUNCION
                            GestorRecursos.setVida(self.jugador.devolverVida())
                            GestorRecursos.setTiempoAcumulado(self.tiempo.obtenerTiempo())
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

        if (jugador.rect.right < MAXIMO_X_JUGADOR/2):

            # Se calcula cuantos pixeles esta fuera del borde
            desplazamiento = jugador.rect.right - MAXIMO_X_JUGADOR/2

            # Si el escenario ya está a la izquierda del todo, no lo movemos mas
            if not self.scrollx <= 2:
                # Calculamos el nivel de scroll actual: el anterior + desplazamiento
                #  (desplazamos a la derecha)
                self.scrollx = self.scrollx + desplazamiento

                return True  # Se ha actualizado el scroll
        return False
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
                    if not enemigo.esUnJefe():
                        self.lesionarPersonaje(bala, enemigo)
                        if not enemigo.tieneVida():
                            enemigo.kill()
                    else:
                        self.accionEspecialJefe(enemigo,bala)
            if pygame.sprite.collide_rect(self.jugador, enemigo):
                self.golpearseEnemigo(enemigo, self.jugador)
    
    def accionEspecialJefe(self,boss,bala):
        if pygame.sprite.collide_rect(boss, bala):
            self.lesionarPersonaje(bala,boss)
            self.listaVidasEnemigo.perderVida(bala.damageBala())
            if not boss.tieneVida():
                GestorRecursos.inicializar()
                self.director.cambiarAlMenu(self, PANTALLA_VICTORIA)

    
    def update(self, tiempo):
        # Primero, se indican las acciones que van a hacer las balas.
        self.moverBalas(self.grupoBalasJugador)
        self.moverBalas(self.grupoBalasSoldado)

        self.colisionEnemigoBalaAmiga(self.grupoSoldados, tiempo)
        self.colisionEnemigoBalaAmiga(self.grupoZombies, tiempo)

        #Cronometro 
        self.cronometro = pygame.time.get_ticks() / 1000 - self.cronometroScene - self.tiempoEnPausa
        if self.cronometro < 0:
            self.cronometro = 0

        self.tiempo.actualizarCronometro(self.cronometro)

        if(self.cronometro == self.tiempoFase):
            GestorRecursos.inicializar()
            self.director.cambiarAlMenu(self, PANTALLA_GAMEOVER)
        
        self.grupoSpritesDinamicos.update(self.grupoPlataformas, tiempo)

        #Fondo
        self.fondo.update(tiempo)

        #--------------------- Comprobamos si hay colisión entre algún jugador
        for bala in self.grupoBalasSoldado:
            if pygame.sprite.collide_rect(self.jugador, bala):
                # Si chocan se lesiona al personaje.
                self.lesionarPersonaje(bala, self.jugador)

        #----------------------Comprobar que el jugador esta muerto
        if not self.jugador.tieneVida():
            GestorRecursos.inicializar()
            self.director.cambiarAlMenu(self, PANTALLA_GAMEOVER)

        #----------------------Comprobar que el jugador choca con algun kit de curacion
        for kitCurativo in self.kitsCurativos:
            if pygame.sprite.collide_rect(self.jugador, kitCurativo):
                valorKitCurativo = kitCurativo.recogerKitCurativo()
                self.jugador.recuperarVida(valorKitCurativo)
                self.vida.recuperarVida(valorKitCurativo)
                kitCurativo.vaciar()

        # ---------------------Comprobamos si hay colision entre algun jugador y el objeto principal
        if GestorRecursos.getConfiguration('TIENE_OBJETO_PRINCIPAL') == True:
            if pygame.sprite.collide_rect(self.jugador, self.objeto):
                nombreObjeto = GestorRecursos.getConfiguration('IMAGEN_OBJETO_PRINCIPAL')
                posicion = GestorRecursos.getConfiguration('POSICION_OBJETO_PRINCIPAL')
                objetoInventario = self.objeto.crearObjetoInventario(nombreObjeto)
                self.inventario.guardarObjeto(objetoInventario)
                GestorRecursos.ponerObjeto(posicion-1,nombreObjeto)
                self.objeto.kill()
                self.pasarFase = True
        #-------Collide Barco-------------------------------------------
        if GestorRecursos.getConfiguration('TIENE_BARCO') == True:
            for barco in self.barco:
                if pygame.sprite.collide_rect(self.jugador, barco):
                    GestorRecursos.setVida(self.jugador.devolverVida())
                    GestorRecursos.setTiempoAcumulado(self.tiempo.obtenerTiempo())
                    self.director.cambiarAlMenu(self, PANTALLA_CUTSCENE)

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
        if GestorRecursos.getConfiguration('TIENE_BARCO') == True:
            self.barco.draw(pantalla)
        # Para pintar las balas como un sprite tienen que estar en el grupo de sprites
        # pero es el jugador quien gestiona la existencia de cada uno, por tanto, de grupoSPrites
        # En caso de existir disparos por parte del jugador se dibujan.
        self.agregarDisparosEscena(self.jugador, self.grupoBalasJugador)

        # En caso de que los enemigos tengan disparos que dar se dibujan.
        for enemigo in self.grupoSoldados:
            self.agregarDisparosEscena(enemigo, self.grupoBalasSoldado)

        # Finalmente se pinta el grupo de sprites.
        #self.grupoSprites.draw(pantalla)
        self.grupoObjetos.draw(pantalla)
        self.grupoEnemigos.draw(pantalla)
        self.grupoJugador.draw(pantalla)
        self.grupoBalasJugador.draw(pantalla)
        self.grupoBalasSoldado.draw(pantalla)
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
                    GestorRecursos.setTiempoAcumulado(self.tiempo.obtenerTiempo())
                    self.director.cambiarAlMenu(self, PANTALLA_CUTSCENE)
                #--------------MENU PAUSA-------------------------
                elif evento.key == K_p:
                    self.tiempoAntesDePausa = pygame.time.get_ticks() / 1000 - self.cronometroScene
                    self.director.cambiarAlMenu(self, PANTALLA_PAUSA)
                #--------------VICTORIA-------------------------------
                elif evento.key == K_v:
                    GestorRecursos.inicializar()
                    self.director.cambiarAlMenu(self, PANTALLA_VICTORIA)
                #--------------GAME_OVER-------------------------
                elif evento.key == K_g:
                    GestorRecursos.inicializar()
                    self.director.cambiarAlMenu(self, PANTALLA_GAMEOVER)
                #---------------DISPARAR--------------------------
                """elif evento.key == K_t:
		    self.jugador.dispararBala()"""
            if evento.type == pygame.QUIT:
                self.director.salirPrograma()

        teclasPulsadas = pygame.key.get_pressed()
        self.jugador.mover(teclasPulsadas, GestorRecursos.getConfigParam('teclas')['ARRIBA'],GestorRecursos.getConfigParam('teclas')['ABAJO'],
        GestorRecursos.getConfigParam('teclas')['IZQUIERDA'], GestorRecursos.getConfigParam('teclas')['DERECHA'], GestorRecursos.getConfigParam('teclas')['DISPARAR'])

   
    def obtenerNumeroFaseSiguiente(self):
        return self.numFaseSiguiente





