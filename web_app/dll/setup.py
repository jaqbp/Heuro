from setuptools import setup
from Cython.Build import cythonize
from setuptools.command.build_ext import build_ext
import numpy as np
import os
import glob


# To nie działa, bo permisje na windowsie to żart
class CustomBuildExt(build_ext):
    def run(self):
        self.run_function_before_build()
        build_ext.run(self)

    def run_function_before_build(self):
        for file in glob.glob("*.pyd"):
            os.remove(
                file,
            )


setup(
    ext_modules=cythonize("custom_function.pyx", language_level="3"),
    cmdclass={"build_ext": CustomBuildExt},
    include_dirs=[np.get_include()],
)
