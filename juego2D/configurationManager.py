
from ConfigParser import *
import logging, sys, os

#CLASE DEDICADA A LA LECTURA DE CONFIGURACION.
#INICIALMENTE DE UN SOLO FICHERO, SE PRETENDE IMPLEMENTAR POSIBILIDAD DE VARIOS

class ConfigurationManager(object):
    #CONFIGURACION DEL LOG PARA CONFIGURATION MANAGER
    logger = logging.getLogger('confManager')
    path = os.path.join('conf/log/', 'confManager.log')
    hdlr = logging.FileHandler(path)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr) 
    logger.setLevel(logging.DEBUG)    
    
    #PRUEBA CARGA FICHERO CONFIGURACION
    @classmethod
    def loadConfigData(cls,section,field):
        path = os.path.join('conf/', 'screenTexts.ini')
        config = ConfigParser()
        config.read(path)
        option = config.get(section,field)
        cls.logger.info('We have an option: %s',option)

