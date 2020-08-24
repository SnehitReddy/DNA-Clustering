from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize

diff_extension = Extension(
    name="pydiff",
    sources=["pydiff.pyx"],
    libraries=["diff"],
    library_dirs=["lib"],
    include_dirs=["lib"]
)
setup(
    name="pydiff",
    ext_modules=cythonize([diff_extension])
)
