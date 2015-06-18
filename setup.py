from setuptools import setup

setup(name='pybs',
      version='0.3',
      description='A library for computing with trees and B-series',
      classifiers=[
        'Programming Language :: Python :: 2.7',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Mathematics ',
      ],
      keywords='B-series rooted tree trees Butcher ',
      url='http://github.com/henriksu/pybs',
      author='Henrik Sperre Sundklakk',
      author_email='henrik.sundklakk@gmail.com',
      packages=['pybs'],
    install_requires=[
          'numpy', 'scipy', 'enum34'
      ],
    test_suite='nose.collector',
    tests_require=['nose'],
      include_package_data=True,
      zip_safe=False)
