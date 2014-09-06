# This Python file uses the following encoding: utf-8
import numpy as np
from fractions import Fraction
from rungekutta import RK_method


RKeuler = RK_method(np.array([[0]], dtype=object),
                    np.array([1], dtype=object))

RKimplicitEuler = RK_method(np.array([[1]], dtype=object),
                            np.array([1], dtype=object)) #  Also known as backward Euler.

RKmidpoint = RK_method(np.array([[0, 0], [Fraction(1, 2), 0]], dtype=object),
                       np.array([0, 1], dtype=object))

RKimplicitTrapezoidal = RK_method(np.array([[0, 0], [Fraction(1,2), Fraction(1,2)]], dtype=object),
                                  np.array([Fraction(1,2), Fraction(1,2)], dtype=object))

RKimplicitMidpoint = RK_method(np.array([[Fraction(1,2)]], dtype=object),
                               np.array([1], dtype=object))

# The two folloving are given at the top of page 30 in Hairer, Lubich, Wanner. Due to Runge.
RKrunge1 = RK_method(np.array([[0, 0], [1, 0]], dtype=object),
                     np.array([Fraction(1,2), Fraction(1,2)], dtype=object)) #  Also known as Heun's method.

RKrunge2 = RK_method(np.array([[0, 0], [Fraction(1,2), 0]], dtype=object),
                     np.array([0, 1], dtype=object))

RK4 = RK_method(np.array([[0,0,0,0],[Fraction(1,2), 0,0,0],[0, Fraction(1,2),0,0],[0,0,1,0]], dtype=object),
                np.array([1,2,2,1], dtype=object) * Fraction(1,6))

RK38rule = RK_method(np.array([[0, 0, 0, 0],[Fraction(1, 3), 0, 0, 0],[Fraction(-1, 3), 1, 0, 0],[1, -1, 1, 0]], dtype=object),
                     np.array([1, 3, 3, 1], dtype=object) * Fraction(1, 8))

RKlobattoIIIA4 = RK_method(np.array([[0, 0, 0],[Fraction(5, 24), Fraction(1, 3), Fraction(-1, 24)],[Fraction(1, 6), Fraction(2, 3), Fraction(1, 6)]], dtype=object),
                           np.array([1, 4, 1], dtype=object) * Fraction(1, 6))

RKlobattoIIIB4 = RK_method(np.array([[Fraction(1, 6), Fraction(-1, 6), 0],[Fraction(1, 6), Fraction(1, 3), 0],[Fraction(1, 6), Fraction(5, 6), 0]], dtype=object),
                           np.array([1, 4, 1], dtype=object) * Fraction(1, 6))

RKcashKarp = RK_method(
    np.array(
   [[0, 0, 0, 0, 0, 0],
    [Fraction(1, 5), 0, 0, 0, 0, 0],
    [Fraction(3, 40), Fraction(9,40), 0, 0, 0, 0],
    [Fraction(3, 10), Fraction(-9, 10), Fraction(6, 5), 0, 0, 0],
    [Fraction(-11, 54), Fraction(5, 2), Fraction(-70, 27), Fraction(35, 27), 0, 0],
    [Fraction(1631, 55296), Fraction(175, 512), Fraction(575, 13824), Fraction(44275, 110592), Fraction(253, 4096), 0]],
              dtype=object),\
    np.array([Fraction(37, 378), 0, Fraction(250, 621), Fraction(125, 594), 0, Fraction(512, 1771)], dtype=object))
