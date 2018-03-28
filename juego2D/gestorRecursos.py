# -*- encoding: utf-8 -*-
import pygame, sys, os
from pygame.locals import *

class GestorRecursos(object):
    recursos = {}
    
    Nivel_Bosque = {'NOMBRE': 'BOSQUE', 'PLATAFORMA': (0, 400, 1200, 15), 'PASAR_FASE': False,
                   'ENEMIGOS': [('Soldado',300),('Soldado',1000),('Zombie',500),('Zombie',700)],
                    'KIT_CURACION': [(20,160)],
                    'PLATAFORMA_SECUNDARIA': [('Caja',200,401),('Caja',10,401),('Caja',900,401)],
                    'POSICION_OBJETO_PRINCIPAL': 1,
                    'COORDENADAS_OBJETO_PRINCIPAL': 300, #Actualmente no se usa
                    'IMAGEN_OBJETO_PRINCIPAL': 'bidonGasolina',
                    'TIEMPO':30} #Lo primero es la vida que carga (multiplos de diez, posicionX)
                    
    Nivel_Playa = {'NOMBRE': 'PLAYA', 'PLATAFORMA': (0, 480, 1200, 15), 'PASAR_FASE': True, 
                   'ENEMIGOS': [('Soldado',350)],
                   'KIT_CURACION': [(20,600),(20,120)],
                   'PLATAFORMA_SECUNDARIA': [('Caja',200,481),('Caja',10,481),('Caja',900,481)],
                   'BARCO': [('Barco',1000,481)],
                   'TIENE_BARCO': True,
                   'TIEMPO': 20}

    Nivel_Pasillo_Bunker =  {'NOMBRE': 'BUNKER', 'PLATAFORMA': (0, 455, 1200, 15), 'TIENE_OBJETO_PRINCIPAL': True, 
                    'ENEMIGOS': [('Soldado',600)], 
                     'KIT_CURACION': [(20,10)],
                     'PLATAFORMA_SECUNDARIA': [('Caja',200,456)],
                     'COORDENADAS_OBJETO_PRINCIPAL': 456, #Actualmente no se usa
                     'IMAGEN_OBJETO_PRINCIPAL': 'llave',
                     'POSICION_OBJETO_PRINCIPAL': 2,
                     'TIEMPO': 20}    


    Nivel_Bunker =  {'NOMBRE': 'BUNKER', 'PLATAFORMA': (0, 455, 1200, 15), 
                    'ENEMIGOS': [('Boss', 1000)], 
                     'KIT_CURACION': [(20,10)],
                     'PLATAFORMA_SECUNDARIA': [('Caja',200,401),('Caja',10,401),('Caja',900,401)],
                     'TIENE_BOSS': True,
                     'TIEMPO': 40}    

    config = {'teclas': {'ARRIBA': K_w, 'ABAJO': K_s, 'IZQUIERDA': K_a, 'DERECHA': K_d, 'DISPARAR': K_j},
              '1': Nivel_Bosque,
              '2': Nivel_Playa,
              '3': Nivel_Pasillo_Bunker,
              '4': Nivel_Bunker,
              }
    
    vida = 1000
    inventario = ['bidonGasolinaSinConseguir','llaveSinConseguir']

    @classmethod
    def CargarImagen(cls, nombre, colorClave=None):
        if nombre in cls.recursos: #Si ya está cargado
            return cls.recursos[nombre] #Se devuelve
        else: #si no
            nombreEntero = os.path.join('imagenes/', nombre) #Se carga
            try:
                imag = pygame.image.load(nombreEntero) #intentamos cargar
            except pygame.error, message:
                print 'No se ha podido cargar', nombreEntero
                raise SystemExit, message
            imag = imag.convert()
            if colorClave is not None: 
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
        try:
            return cls.configuration[param]
        except KeyError:
            return False

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

    @classmethod
    def inicializar(cls):
        cls.vida = 1000
        cls.inventario = ['bidonGasolinaSinConseguir','llaveSinConseguir']

    @classmethod
    def ponerObjeto(cls,posicion,nombreObjeto):
        cls.inventario[posicion] = nombreObjeto

    @classmethod
    def getInventario(cls):
        return cls.inventario




