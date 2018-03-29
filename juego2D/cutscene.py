# -*- encoding: utf-8 -*-
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
from fase import *

SUCESS = None

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
        # Si ya no hay texto que actualizar termina la cutscene
        if (self.actualizarTextoTituloNivel() == None):
            self.crearSceneSiguiente()


    def dibujar(self, pantalla):
        # Ponemos primero el fondo
        self.fondoCutScene.dibujar(pantalla)

    # Crea la fase siguiente, teniendo en cuenta que tiene el mismo número que esta fase.
    # Además sale de está pantalla de cutScene e inicializa el cronómetro de la fase nueva.
    def crearSceneSiguiente(self):
        self.director.salirEscena()
        faseNueva = Fase(self.director, self.numFase)
        faseNueva.cronometroScene = pygame.time.get_ticks() / 1000
        self.director.apilarEscena(faseNueva)

    #Actualiza la posición del texto del título de nivel.
    def actualizarTextoTituloNivel(self):
        # Actualizar el texto que corresponda.
        (posicion, _) = self.fondoCutScene.update(
            self.movimientoPosicion, self.texto)
        if posicion == None:
            return None
        if posicion > 400:  # Cuando llega más o menos a la mitad del texto el titulo...:
            self.mostrarTexto()  # Se muestra el otro texto.
            self.movimientoPosicion = 1  # Se baja la velocidad
        return 1


    # Dependiendo de cual de estas funciones sean se muestra el texto texto o
    # texto de titulo.
    def mostrarTexto(self):
        self.texto = TEXTO

    def mostrarTitulo(self):
        self.texto = TITULO



class FondoCutScene:
    def __init__(self, nombreFase):
        GestorRecursos.setConfiguration(nombreFase[1])
        self.imagen = GestorRecursos.CargarImagen(
            'Cutscene' + nombreFase + '/Nivel.jpg', 1)
        self.imagen = pygame.transform.scale(
            self.imagen, (ANCHO_PANTALLA, ALTO_PANTALLA))
        #Texto de título nivel necesita saber cual es el nombre de la fase.
        self.textoTitulo = TextoTituloNivel(self, (nombreFase[1] + " : " + GestorRecursos.getConfiguration('NOMBRE')))
        # Inicialmente vacio, lo cargaremos de un fichero de texto.
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
        # Si lo que hay que updatear es el titulo, se mueve su posición x
        if self.texto == TITULO:
            return self.textoTitulo.moverPosicion(x=movimientoPosicion)
        # Pero si lo que hay que updatear es el texto, se mueve su posición y.
        elif self.texto == TEXTO:
            # Hay que mover cada una de las líneas del texto.
            for lineaTextoNivel in self.textoNivel:
                lineaTextoNivel.moverPosicion(y=movimientoPosicion)
            
            #Cuando llegue a un punto la última línea, definido en el gestor de recursos individual para cada pantalla proque
            # cada una tiene una longitud del texto, entonces terminamos la escena. 
            if (self.textoNivel[len(self.textoNivel)-1].posicionY() == GestorRecursos.getConfiguration('DURACION_CUTSCENE')):
                return (SUCESS,"Hemos terminado de imprimir el texto del nivel")
            return (0, 0)

    def dibujar(self, pantalla):
        # Dibujamos primero la imagen de fondo
        pantalla.blit(self.imagen, self.imagen.get_rect())
        # Si es el titulo se dibuja el titulo.
        if self.texto == TITULO:
            self.textoTitulo.dibujar(pantalla)    
        # Si es el texto se dibuja el texto.                 
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