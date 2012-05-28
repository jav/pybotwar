import os

from PyQt4 import QtCore, QtSvg

def makeconf():
    'create an empty conf file'

    conf_file = 'conf.py'

    if os.path.exists(conf_file):
        print 'conf.py already exists'
        raise SystemExit

    contents = '''\
# Change configuration settings here.
# See defaults.py for the default settings

from defaults import *


'''

    f = open(conf_file, 'w')
    f.write(contents)
    f.close()

    print 'conf.py created'
    print 'please check configuration.'


from collections import defaultdict

class defaultNonedict(defaultdict):
    def __missing__(self, key):
        return None


def get_robot_dirs():
    import conf
    try:
        from PyQt4 import QtCore
        useQtSettings = True
    except ImportError:
        useQtSettings = False

    if useQtSettings:
        QtCore.QCoreApplication.setOrganizationName('pybotwar.googlecode.com')
        QtCore.QCoreApplication.setOrganizationDomain('pybotwar.googlecode.com')
        QtCore.QCoreApplication.setApplicationName('pybotwar')
        settings = QtCore.QSettings()
        settings.sync()

        d = settings.value('pybotwar/robotdir', '').toString()
        if d and conf.robot_dirs and d != conf.robot_dirs[0]:
            conf.robot_dirs.insert(0, str(d))

    return conf.robot_dirs
    
    
class SvgRenderer(object):
    'factory for svg renderer objects'

    def __init__(self, app):
        self.app = app

    def getrend(self, filepath=None):
        '''return a handle to the shared SVG renderer
            for the given svg file.

        If no filepath is given, return the renderer for
            the default svg file.

        '''
        if filepath is None:
            datadir = 'data'
            filename = 'robot.svg'
            filepath = os.path.join(datadir, 'images', filename)
        fp = QtCore.QString(filepath)
        rend = QtSvg.QSvgRenderer(fp, self.app)
        return rend

