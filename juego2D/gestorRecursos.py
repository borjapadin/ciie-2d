# -*- encoding: utf-8 -*-
import pygame, sys, os
from pygame.locals import *

class GestorRecursos(object):
    recursos = {}
    
    Nivel_Bosque = {'NOMBRE': 'BOSQUE', 'PLATAFORMA': (0, 400, 1200, 15), 'OBJETO_PRINCIPAL': ('bidonGasolina',750,1), 'PASAR_FASE': False,
                    'ENEMIGOS': [('Soldado',300),('Soldado',400),('Zombie',500),('Zombie',700)],
                    'KIT_CURACION': [(20,450),(70,650)]} #Lo primero es la vida que carga (multiplos de diez, posicionX)
    Nivel_Playa = {'NOMBRE': 'PLAYA', 'PLATAFORMA': (0, 480, 1200, 15), 'OBJETO_PRINCIPAL':  (None,None,None), 'PASAR_FASE': True, 
                   'ENEMIGOS': [('Soldado',350)],
                   'KIT_CURACION': [(20,600),(20,120)]}
    Nivel_Bunker =  {'NOMBRE': 'BUNKER', 'PLATAFORMA': (0, 455, 1200, 15), 'OBJETO_PRINCIPAL': ('llave',300,2), 'PASAR_FASE': False, 
                     'ENEMIGOS': [('Soldado',600)],
                     'KIT_CURACION': [(20,10)]}    
    
    config = {'teclas': {'ARRIBA': K_w, 'ABAJO': K_s, 'IZQUIERDA': K_a, 'DERECHA': K_d, 'DISPARAR': K_j},
              '1': Nivel_Bosque,
              '2': Nivel_Playa,
              '3': Nivel_Bunker,
              }
    vida = 1000

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

    @classmethod
    def setConfiguration(cls,numFase):
        cls.configuration = cls.getConfigParam(numFase)

    @classmethod
    def getConfiguration(cls,param):
        return cls.configuration[param]

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
    
    @classmethod
    def setVida(cls,vida):
        cls.vida = vida

    @classmethod
    def getVida(cls):
        return cls.vida


