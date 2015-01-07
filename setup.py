from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()


def _license():
    with open('LICENSE') as f:
        return f.read()


setup(name='pybs',
      version='0.1',
      description='A library for computing with trees and B-series',
      long_description=readme(),
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Mathematics ',
      ],
      keywords='B-series rooted tree trees Butcher ',
      url='http://github.com/henriksu/pybs',
      author='Henrik Sperre Sundklakk',
      author_email='henrik.sundklakk@gmail.com',
      license=_license(),
      packages=['pybs'],
    install_requires=[
          'numpy',
      ],
    test_suite='nose.collector',
    tests_require=['nose'],
      include_package_data=True,
      zip_safe=False)