Multisets
==========

.. currentmodule:: pybs.utils.clonable_multiset

.. autoclass:: ClonableMultiset(Clonable)

   .. automethod:: ClonableMultiset.__init__

   .. automethod:: ClonableMultiset.__copy__

   .. automethod:: ClonableMultiset.__nonzero__

   .. automethod:: ClonableMultiset.__contains__

   .. automethod:: ClonableMultiset._hash_

   .. automethod:: ClonableMultiset.__repr__

   Setting and getting values is done as for a dictionary, with the following exeptions:

      * Only natural numbers are allowed as values.
      * If a value is set to 0, the key is deleted.
      * Deleting a nonexistent key does noting.
      * Retriveing a nonexistent key returns 0.

   .. automethod:: ClonableMultiset.cardinality

   .. automethod:: ClonableMultiset.no_uniques

   .. automethod:: ClonableMultiset.most_common

   The ``==`` and ``!=`` operators are overloaded to compare ClonableMultisets for equality. The test is based on equality of the underlying dicitonaries.

   .. automethod:: ClonableMultiset.elements

   .. automethod:: ClonableMultiset.keys

   .. automethod:: ClonableMultiset.values

   .. automethod:: ClonableMultiset.items

Operations between Multisets
-----------------------------
   .. automethod:: ClonableMultiset.sub

   .. automethod:: ClonableMultiset.__and__

   .. automethod:: ClonableMultiset.__or__

   .. automethod:: ClonableMultiset.inplace_multiset_sum	

   .. automethod:: ClonableMultiset.multiset_sum

   .. automethod:: ClonableMultiset.scalar_mul

   .. automethod:: ClonableMultiset.inplace_multiset_difference

   .. automethod:: ClonableMultiset.multiset_difference

   .. automethod:: ClonableMultiset.inplace_add

   .. automethod:: ClonableMultiset.add



