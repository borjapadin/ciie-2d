
import logging, sys, os

class loggerCreator(object):

	#PROVIDES QUICK IMPLEMENTATION OF A LOGGER FOR A FILE
	@classmethod
	def getLogger(cls,loggerName,logFileName):
		#CONFIGURACION DEL LOGGER
	    logger = logging.getLogger(loggerName)
	    path = os.path.join('conf/log/', logFileName)
	    hdlr = logging.FileHandler(path)
	    #FORMATO POR DEFECTO FECHA - NIVEL DE GRAVEDAD - MENSAJE
	    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
	    hdlr.setFormatter(formatter)
	    logger.addHandler(hdlr) 
	    ##SETS THE LOGGING LEVEL
	    logger.setLevel(logging.DEBUG)  
	    return logger  
    