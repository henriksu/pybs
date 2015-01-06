# This Python file uses the following encoding: utf-8
import numpy as _np
from fractions import Fraction as _Fraction

from rk_method import RK_method as _RK


RKeuler = _RK(_np.array([[0]], dtype=object),
              _np.array([1], dtype=object))

RKimplicitEuler = _RK(_np.array([[1]], dtype=object),
                      _np.array([1], dtype=object))
# Also known as backward Euler.

RKmidpoint = _RK(_np.array([[0, 0], [_Fraction(1, 2), 0]], dtype=object),
                 _np.array([0, 1], dtype=object))

RKimplicitTrapezoidal = _RK(_np.array([[0, 0],
                                       [_Fraction(1, 2), _Fraction(1, 2)]],
                                      dtype=object),
                            _np.array([_Fraction(1, 2), _Fraction(1, 2)],
                                      dtype=object))

RKimplicitMidpoint = _RK(_np.array([[_Fraction(1, 2)]], dtype=object),
                         _np.array([1], dtype=object))

# The two folloving are given at the top of page 30 in
# Hairer, Lubich, Wanner. Due to Runge.
RKrunge1 = _RK(_np.array([[0, 0], [1, 0]], dtype=object),
               _np.array([_Fraction(1, 2), _Fraction(1, 2)], dtype=object))
#  Also known as Heun's method.

RKrunge2 = _RK(_np.array([[0, 0], [_Fraction(1, 2), 0]], dtype=object),
               _np.array([0, 1], dtype=object))

RK4 = _RK(_np.array([[0, 0, 0, 0], [_Fraction(1, 2), 0, 0, 0],
                     [0, _Fraction(1, 2), 0, 0], [0, 0, 1, 0]], dtype=object),
          _np.array([1, 2, 2, 1], dtype=object) * _Fraction(1, 6))

RK38rule = _RK(_np.array([[0, 0, 0, 0], [_Fraction(1, 3), 0, 0, 0],
                          [_Fraction(-1, 3), 1, 0, 0], [1, -1, 1, 0]],
                         dtype=object),
               _np.array([1, 3, 3, 1], dtype=object) * _Fraction(1, 8))

RKlobattoIIIA4 = _RK(_np.array([[0, 0, 0], [_Fraction(5, 24), _Fraction(1, 3),
                                _Fraction(-1, 24)], [_Fraction(1, 6),
                                _Fraction(2, 3),
                                _Fraction(1, 6)]], dtype=object),
                     _np.array([1, 4, 1], dtype=object) * _Fraction(1, 6))

RKlobattoIIIB4 = _RK(_np.array([[_Fraction(1, 6), _Fraction(-1, 6), 0],
                                [_Fraction(1, 6), _Fraction(1, 3), 0],
                                [_Fraction(1, 6), _Fraction(5, 6), 0]],
                               dtype=object),
                     _np.array([1, 4, 1], dtype=object) * _Fraction(1, 6))

RKcashKarp = _RK(
    _np.array(
        [[0, 0, 0, 0, 0, 0],
         [_Fraction(1, 5), 0, 0, 0, 0, 0],
         [_Fraction(3, 40), _Fraction(9, 40), 0, 0, 0, 0],
         [_Fraction(3, 10), _Fraction(-9, 10), _Fraction(6, 5), 0, 0, 0],
         [_Fraction(-11, 54), _Fraction(5, 2), _Fraction(-70, 27),
          _Fraction(35, 27), 0, 0],
         [_Fraction(1631, 55296), _Fraction(175, 512), _Fraction(575, 13824),
          _Fraction(44275, 110592), _Fraction(253, 4096), 0]],
        dtype=object),
    _np.array([_Fraction(37, 378), 0, _Fraction(250, 621), _Fraction(125, 594),
               0, _Fraction(512, 1771)], dtype=object))
