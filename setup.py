from setuptools import setup

setup(name='pybs',
      version='0.1',
      description='A library for computing with trees and B-series',
      url='http://github.com/henriksu/pybs',
      author='Henrik Sperre Sundklakk',
      author_email='henrik.sundklakk@gmail.com',
      license='MIT',
      packages=['pybs'],
    install_requires=[
          'numpy',
      ],
      zip_safe=False)