
from ConfigParser import *
from loggerCreator import *

#CLASE DEDICADA A LA LECTURA DE CONFIGURACION.
#INICIALMENTE DE UN SOLO FICHERO, SE PRETENDE IMPLEMENTAR POSIBILIDAD DE VARIOS

class ConfigurationManager(object):
    
    #PRUEBA CARGA FICHERO CONFIGURACION
    @classmethod
    def loadConfigData(cls,section,field):
        path = os.path.join('conf/', 'screenTexts.ini')
        config = ConfigParser()
        config.read(path)
        option = config.get(section,field)
        logger = loggerCreator.getLogger('configurationLog','confManager.log')
        logger.info('We have an option: %s',option)
        return option

