# -*- encoding: utf-8 -*-
import pygame, sys, os
from pygame.locals import *

class GestorRecursos(object):
    recursos = {}
    
    Nivel_Bosque = {'NOMBRE': 'Bosque', 'PLATAFORMA': (0, 400, 1200, 15), 'PASAR_FASE': False,
                   'ENEMIGOS': [('Soldado',200,401),('Soldado',390,363),('Soldado',500,401),
                                ('Soldado',750,401),('Soldado',900,401),('Soldado',930,363)],
                    'KIT_CURACION': [(100,390,333),(100,520,401)], # VIDA, X, Y
                    'PLATAFORMA_SECUNDARIA': [('Caja',210,411),('Caja',380,411),('Caja',380,374),('Caja',900,411)],
                    'POSICION_OBJETO_PRINCIPAL': 1,
                    'COORDENADAS_OBJETO_PRINCIPAL': (850,402), #Actualmente no se usa
                    'IMAGEN_OBJETO_PRINCIPAL': 'bidonGasolina',
                    'TIEMPO': 20,
                    'DURACION_CUTSCENE':1400,
                    'TIENE_OBJETO_PRINCIPAL': True,
                    'POSICION_DECORADO' : (1200, 400),
                    'MUSICA_AMBIENTE': 'Nivel_1_Bosque.mp3'} #Lo primero es la vida que carga (multiplos de diez, posicionX)
                    
    Nivel_Playa = {'NOMBRE': 'Playa', 'PLATAFORMA': (0, 480, 1200, 15), 'PASAR_FASE': True, 
                   'ENEMIGOS': [('Soldado',380,440),('Soldado',530,481),('Soldado',730,440),
                                ('Soldado',880,481),('Zombie',300,480),
                                ('Zombie',400,481),('Zombie',500,481),('Zombie',600,481),
                                ('Zombie',700,481),('Zombie',750,481),('Zombie',800,481)],
                   'KIT_CURACION': [(100,370,450),(100,720,450)], # VIDA, X, Y
                   'PLATAFORMA_SECUNDARIA': [('Caja',350,490),('Caja',700,490)],
                   'BARCO': [('Barco',1000,481)],
                   'TIENE_BARCO': True,
                   'TIEMPO':20,
                   'DURACION_CUTSCENE': 1400,
                   'POSICION_DECORADO' : (1200, 400),
                   'MUSICA_AMBIENTE': 'Nivel_2_Playa.mp3'}

    Nivel_Pasillo_Bunker =  {'NOMBRE': 'Bunker', 'PLATAFORMA': (0, 455, 1200, 15), 'TIENE_OBJETO_PRINCIPAL': True,
                    'PASAR_FASE': False,
                    'ENEMIGOS': [('Soldado',200,455),('Soldado',425,405),('Soldado',600,455),('Soldado',825,405),
                                ('Soldado',825,371),('Soldado',825,455),('Soldado',1025,455),('Soldado',1025,371),('Soldado',1025,405),
                                ('Zombie',300,455),('Zombie',350,455),('Zombie',400,405),('Zombie',450,455),
                                ('Zombie',500,455),('Zombie',550,455),('Zombie',600,455),('Zombie',650,455),
                                ('Zombie',900,455),('Zombie',920,455),('Zombie',950,455),('Zombie',970,455)], 
                     'KIT_CURACION': [(100,440,456), (100,800,456)],
                     'PLATAFORMA_SECUNDARIA': [('Caja',400,456),('Caja',800,456),('Caja',800,420),('Caja',1000,456),('Caja',1000,420)],
                     'COORDENADAS_OBJETO_PRINCIPAL': (925,452), #Actualmente no se usa
                     'IMAGEN_OBJETO_PRINCIPAL': 'llave',
                     'POSICION_OBJETO_PRINCIPAL': 2,
                     'TIEMPO':40,
                     'DURACION_CUTSCENE': 1600,'CURAR_VIDA':True,
                     'POSICION_DECORADO' :  (1200, 350),
                     'MUSICA_AMBIENTE': 'Nivel_3_Bunker.mp3'}    


    Nivel_Bunker =  {'NOMBRE': 'Sala del boss', 'PLATAFORMA': (0, 440, 1200, 15), 'PASAR_FASE':False,
                    'ENEMIGOS': [('Boss', 700, 441)], 
                     'KIT_CURACION': [(100,114,368),(100,614,368),(100,1114,368)],
                     'PLATAFORMA_SECUNDARIA': [('Caja',100,445),('Caja',100,409),('Caja',600,445),
                                            ('Caja',600,409),('Caja',1100,445),('Caja',1100,409)],
                     'TIENE_BOSS': True,
                     'TIEMPO':40,
                     'DURACION_CUTSCENE':1100,
                     'POSICION_DECORADO' :  (1200, 350),
                     'MUSICA_AMBIENTE': 'Nivel_4_Boss.mp3'
                     }    

    config = {'teclas': {'ARRIBA': K_w, 'ABAJO': K_s, 'IZQUIERDA': K_a, 'DERECHA': K_d, 'DISPARAR': K_j},
              '1': Nivel_Bosque,
              '2': Nivel_Playa,
              '3': Nivel_Pasillo_Bunker,
              '4': Nivel_Bunker,
              }
    
    # Objetos persistentes llamemoslos
    tiempoAcumulado = 0
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
    def CargarMusica(cls, nombre):
        if nombre in cls.recursos:
                return cls.recursos[nombre]
        else:
            nombreEntero = os.path.join('musica', nombre)
            try:
                sound = pygame.mixer.music.load(nombreEntero)
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
    def setTiempoAcumulado(cls,tiempo):
        cls.tiempoAcumulado = tiempo

    @classmethod
    def getTiempoAcumulado(cls):
        return cls.tiempoAcumulado

    @classmethod
    def inicializar(cls):
        cls.vida = 1000
        cls.inventario = ['bidonGasolinaSinConseguir','llaveSinConseguir']
        cls.tiempoAcumulado = 0

    @classmethod
    def ponerObjeto(cls,posicion,nombreObjeto):
        cls.inventario[posicion] = nombreObjeto

    @classmethod
    def getInventario(cls):
        return cls.inventario




