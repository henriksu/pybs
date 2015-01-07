=====
PyBS
=====
----------------------
Python Butcher-Series
----------------------
.. contents::

What is PyBS?
--------------

PyBS is a library for computing with trees and B-series written i Python.
It contains classes to represent unlabeled unordered rooted trees, forests and other related structures.
The purpose is to automate calculations needed when analyzing numerical methods for ordinary differential equations.

The library includes basic functions on trees such as order, density and symmetry.
Classes representing forests and linear combinations of trees are offered
along with functions to graft one tree onto another, calculate the tree commutator,
and finding the splittings of a tree.
Butcher series are represented by functions from the set of trees to the real numbers.
Functionality includes composition with h · f (·), the Lie derivative,
the series of the modified equation,
and the series of a Runge-Kutta method given its Butcher tableau.

Installation
-------------
PyBS is available on PyPI. It may be installed with pip by executing

``$ pip install pybs``

in the terminal.
Alternatively one can dowload the repository and execute

``$ python setup.py install``

or

``$ python setup.py develop``

from the outermost pybs-directory.

Documentation
--------------

The report from the author's specialization project gives an overview.
In addition reading and running ``pybs/pybs/examples.py`` as well as the tests found in ``pybs/pybs/test/`` can be useful.

Contact
--------
PyBS is developed as a part of the master's thesis of Henrik Sperre Sundklakk, henrik.sundklakk@gmail.com,
supervised by professor Brynjulf Owren, Department of Mathematical Sciences,
Norwegian University of Science and Technology (NTNU), Trondheim.
