from distutils.core import setup
from Cython.Build import cythonize

setup(
    name='R6s Server Switcher',
    ext_modules=cythonize("R6SSS.py")
)