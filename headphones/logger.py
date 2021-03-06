import os
import threading
import logging
from logging import handlers

import headphones

MAX_SIZE = 1000000 # 1mb
MAX_FILES = 5


# Simple rotating log handler that uses RotatingFileHandler
class RotatingLogger(object):

	def __init__(self, filename, max_size, max_files):
	
		self.filename = filename
		self.max_size = max_size
		self.max_files = max_files
		
		
	def initLogger(self, quiet=False):
	
		l = logging.getLogger('headphones')
		l.setLevel(logging.DEBUG)
		
		self.filename = os.path.join(headphones.LOG_DIR, self.filename)
		
		filehandler = handlers.RotatingFileHandler(self.filename, maxBytes=self.max_size, backupCount=self.max_files)
		filehandler.setLevel(logging.DEBUG)
		
		fileformatter = logging.Formatter('%(asctime)s - %(levelname)-7s :: %(message)s', '%d-%b-%Y %H:%M:%S')
		
		filehandler.setFormatter(fileformatter)
		l.addHandler(filehandler)
		
		if not quiet:
		
			consolehandler = logging.StreamHandler()
			consolehandler.setLevel(logging.INFO)
			
			consoleformatter = logging.Formatter('%(asctime)s - %(levelname)s :: %(message)s', '%d-%b-%Y %H:%M:%S')
			
			consolehandler.setFormatter(consoleformatter)
			l.addHandler(consolehandler)	
		
	def log(self, message, level):
	
		logger = logging.getLogger('headphones')
		
		threadname = threading.currentThread().getName()
		message = threadname + ' : ' + message
		
		if level == 'debug':
			logger.debug(message)
		elif level == 'info':
			logger.info(message)
		elif level == 'warn':
			logger.warn(message)
		else:
			logger.error(message)


headphones_log = RotatingLogger('headphones.log', MAX_SIZE, MAX_FILES)

def debug(message):
	headphones_log.log(message, level='debug')

def info(message):
	headphones_log.log(message, level='info')
	
def warn(message):
	headphones_log.log(message, level='warn')
	
def error(message):
	headphones_log.log(message, level='error')
	
