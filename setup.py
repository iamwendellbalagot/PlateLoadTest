# from cx_Freeze import setup, Executable

# setup(name = 'PLTAPP',
# 	  version = '0.1',
# 	  description = 'First Build',
# 	  executables = [Executable('app.py')])

from distutils.core import setup
import py2exe

setup(console=['app.py'])