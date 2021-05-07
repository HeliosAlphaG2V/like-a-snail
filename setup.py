from setuptools import setup, find_packages, Extension

setup(name="Like a snail - LAS",
      version='0.0.1',
      packages=['likeasnail'],
      package_dir={'likeasnail': 'likeasnail'},
      setup_requires=["cffi>=1.0.0"],
      cffi_modules=["./compile/registerCompile.py:ffibuilder"],
      install_requires=["cffi>=1.0.0"]
      )

# cffi_modules=["./compile/registerCompile.py:ffibuilder"],
#  To install data files directly in the target directory,
#  an empty string should be given as the directory.

# packages=['likeasnail', '_register'],
#     package_dir={'likeasnail': 'likeasnail'},

# data_files=[('likeasnail', ['_register/_register.cp37-win_amd64.exp',
#                                  '_register/_register.c', '_register/__init__.py',
#                                  '_register/_register.obj', '_register/_register.cp37-win_amd64.pyd',
#                                  '_register/_register.cp37-win_amd64.lib'])]
