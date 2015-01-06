# This Python file uses the following encoding: utf-8
import unittest

from pybs.rungekutta.methods import *


class RK_library(unittest.TestCase):
    def setUp(self):
        pass

    def test_explicit_Euler(self):
        self.assertEqual(1, RKeuler.order)

    def test_implicit_Euler(self):
        self.assertEqual(1, RKimplicitEuler.order)

    def test_midpoint_rule(self):
        self.assertEqual(2, RKmidpoint.order)

    def test_implicit_trapeziodal_rule(self):
        self.assertEqual(2, RKimplicitTrapezoidal.order)

    def test_implicit_midpoint_rule(self):
        self.assertEqual(2, RKimplicitMidpoint.order)

    def test_Runge_1(self):
        self.assertEqual(2, RKrunge1.order)

    def test_Runge_2(self):
        self.assertEqual(2, RKrunge2.order)

    def test_RK4(self):
        self.assertEqual(4, RK4.order)

    def test_3_8_rule(self):
        self.assertEqual(4, RK38rule.order)

    def test_Lobatto_IIIA4(self):
        self.assertEqual(4, RKlobattoIIIA4.order)

    def test_Lobatto_IIIB4(self):
        self.assertEqual(4, RKlobattoIIIB4.order)

    def test_Cash_Karp(self):
        self.assertEqual(5, RKcashKarp.order)
