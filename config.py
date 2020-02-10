from configparser import ConfigParser
import os, sys


class Config:
    def resource_path(self, relative_path='config\config.ini'):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS

        except Exception:
            base_path = os.path.abspath("")

        print(relative_path)
        return os.path.join(base_path, relative_path)


class BDProperties(Config):

    def __init__(self):
        self.cfgParser = ConfigParser()
        self.cfgParser.read(Config.resource_path(self), encoding=None)

    def getUserName(self):
        return self.cfgParser.get('database_connection', 'name')

    def getPassword(self):
        return self.cfgParser.get('database_connection', 'password')

    def getDataBase(self):
        return self.cfgParser.get('database_connection', 'database')

    def getHost(self):
        return self.cfgParser.get('database_connection', 'host')



