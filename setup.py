from setuptools import setup, find_packages

setup(name="Like a snail - LAS",
      version='0.0.1',
      description='Gameboy emulator',
      author='HeliosAlphaG2V',
      url='https://github.com/HeliosAlphaG2V/like-a-snail',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      include_package_data=True,
      cffi_modules=["./compile/registerCompile.py:ffibuilder"],
      install_requires=["cffi>=1.0.0", "pygame>=2.0.1"]
      )
