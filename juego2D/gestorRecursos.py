# -*- encoding: utf-8 -*-
import pygame, sys, os
from pygame.locals import *

class GestorRecursos(object):
    recursos = {}
    config = {'Generales': {'ARRIBA': K_UP, 'ABAJO': K_DOWN, 'IZQUIERDA': K_LEFT, 'DERECHA': K_RIGHT},
              '1': {'NOMBRE': 'BOSQUE', 'PLATAFORMA': (0, 400, 1200, 15)},
              '2': {'NOMBRE': 'PLAYA', 'PLATAFORMA': (0, 480, 1200, 15)},
              '3': {'NOMBRE': 'BUNKER', 'PLATAFORMA': (0, 455, 1200, 15)},
              }
  #  config = {'ARRIBA': K_UP, 'ABAJO': K_DOWN, 'IZQUIERDA': K_LEFT, 'DERECHA': K_RIGHT,
  #  'BOSQUE_LVL': 0, 'PLAYA_LVL': 0, 'BUNKER_LVL': 0, 
  #  'RATIO': (16,9), 'RES': 600}

    @classmethod
    def CargarImagen(cls, nombre, colorClave=None):
        if nombre in cls.recursos: #Si ya está cargado
            return cls.recursos[nombre] #Se devuelve
        else: #si no
            nombreEntero = os.path.join('imagenes/', nombre) #Se carga
            try:
                imag = pygame.image.load(nombreEntero) #intentamos cargar
                print(nombreEntero)
            except pygame.error, message:
                print 'No se ha podido cargar', nombreEntero
                raise SystemExit, message
            imag = imag.convert()
            if colorClave is not None: #Puse esto (?) aunque no estaba (?) no se si no estaba por algo (?) pero Uxía me mando.
                if colorClave is -1:
                    colorClave = imag.get_at((0,0)) #obtenemos el color base
                imag.set_colorkey(colorClave, RLEACCEL)
            cls.recursos[nombre] = imag #almacenamos
            return imag # lo devolvemos

    @classmethod
    def CargarArchivoCoordenadas(cls,nombre):
        if nombre in cls.recursos: #si ya esta cargado
            return cls.recursos[nombre] #se devuelve
        else: #si no ha sido cargado
            nombreEntero = os.path.join('imagenes', nombre)#se carga
            print (nombreEntero)
            pathfile = open(nombreEntero, 'r') #lo abrimos
            datos = pathfile.read() #lo leemos
            pathfile.close() #lo cerramos
            cls.recursos[nombre] = datos #almacenamos
            return datos #lo devolvemos



	
    @classmethod
    def CargarSonido(cls, nombre):
        if nombre in cls.recursos:
                return cls.recursos[nombre]
        else:
            nombreEntero = os.path.join('sounds', nombre)
            try:
                sound = pygame.mixer.Sound(nombreEntero)
            except pygame.error, message:
                print 'Cannot load sound:', nombreEntero
                raise SystemExit, message
            cls.recursos[nombre] = sound
            return sound


#Config methods 

    #LOADS CONFIG PARAMETERS FROM FILESYSTEM "conf/gameProps.conf"
    @classmethod
    def LoadConfig(cls):
        cofFile = os.path.join('conf', 'gameProps.conf')
        try:
            with open(confFile, 'r') as fp:
                cls.config = json.load(fp)
        except IOError, message:
                print 'Cannot load configuration file:', confFile, ' Creating default file config!'
                cls.SaveConfig()

    #RETRIEVES A PARAMETER FROM CONFIGURATION PARAMETERS LIST
    @classmethod
    def getConfigParam(cls, param):
        if param in cls.config:
            return cls.config[param]
        else:
            return 0

    #MODIFIES THE VALUE OF A CONFIGURATION PARAMETER
    @classmethod
    def setConfigParam(cls, param, value):
        if not param in cls.config:
            cls.config.update({param: value})
        cls.config[param] = value
        cls.SaveConfig()

