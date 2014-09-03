# This Python file uses the following encoding: utf-8
import unittest
from forest import Forest
from trees.ButcherTrees import ButcherTree

class test_Butcher_forest(unittest.TestCase):
	def setUp(self):
		basetree = ButcherTree(Forest())
		self.base_forest = Forest([basetree])

	def test_first(self):
		self.assertEqual('(*^1)',str(self.base_forest))

	def test_second(self):
		forest = self.base_forest.D()
		self.assertEqual('([*]^1)', str(forest))
	
	def test_third(self):
		forest = self.base_forest.D()
		forest = forest.D()
		self.assertEqual('([[*]]^1, [*,*]^1)', str(forest))

	def test_fourth(self):
		forest = self.base_forest.D().D().D()
		self.assertEqual('([[*],*]^3, [[[*]]]^1, [*,*,*]^1, [[*,*]]^1)', str(forest))
	
	def test_fifth(self):
		forest = self.base_forest.D().D().D().D()
# 		expected = '([[*],[*]]^1, [[[*],*]]^3, [[[[*]]]]^1, '+\
# 		'[*,[*,*]]^2, [[*,*,*]]^1, [[[*]],*]^2, [[[*,*]]]^1, '+\
# 		'[[*],*,*]^4, [*,*,*,*]^1)' Old one. probably wrong. TODO: Check manually.
		expected = '([*,[[*]]]^4, [[[[*]]]]^1, [[*,*,*]]^1, '+\
		'[[[*,*]]]^1, [[*],[*]]^3, [*,[*,*]]^4, [[[*],*]]^3, '+\
		'[*,*,*,*]^1, [[*],*,*]^6)'
		self.assertEqual(expected, str(forest))
	
	def test_count_forests(self): #  Also a stress test.
		result = [len(self.base_forest)]
		for i in xrange(11):
			self.base_forest = self.base_forest.D()
			result.append(len(self.base_forest))
		expected = [1, 1, 2, 4, 9, 20, 48, 115, 286, 719, 1842, 4766]
		self.assertListEqual(expected, result)
# In the long run test_count_forests would give
# a=[1, 1, 2, 4, 9, 20, 48, 115, 286, 719, 1842, 4766, 12486, 32973, 87811, 235381, 634847, 1721159]
# When it was finished, about 2GB was used.
# That is on average 1.162 kB per tree. The larges trees had 18 nodes.
# That makes about 70 bytes per node.