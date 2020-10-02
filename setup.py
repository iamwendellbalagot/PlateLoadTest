# import sys
# from cx_Freeze import setup, Executable

# # Dependencies are automatically detected, but it might need fine tuning.
# build_exe_options = {"packages": ["os", 'plotly'], "excludes": ["tkinter", 'matplotlib']}

# # GUI applications require a different base on Windows (the default is for a
# # console application).
# base = None
# if sys.platform == "win32":
#     base = "Win32GUI"

# setup(  name = "PLTAPP",
#         version = "0.1",
#         description = "Civil Engineering Apparatus",
#         options = {"build_exe": build_exe_options},
#         executables = [Executable("app.py", base=base)])

from setuptools import find_packages
from cx_Freeze import setup, Executable
import sys

base = None
if sys.platform == "win32":
    base = "Win32GUI"

includefiles = ['getdata.py', 'createtable.py', 'sqlserver.py', 
				'components/', 'style/', 'excelfiles/', 'databases/']


options = {
    'build_exe': {
        'includes': [
            'cx_Logging', 'idna',
        ],
        'excludes': ['tkinter','matplotlib.tests','numpy.random._examples', 'matplotlib'],
        'include_files': includefiles
    }
}

executables = [
    Executable('app.py',
               base=base,
               targetName='plt_app.exe')
]

setup(
    name='PLTAPP',
    packages=find_packages(),
    version='0.4.0',
    description='rig',
    executables=executables,
    options=options
)