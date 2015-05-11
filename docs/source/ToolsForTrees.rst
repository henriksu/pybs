Tools for Trees
================

.. currentmodule:: pybs.unordered_tree.unordered_trees

.. autoclass:: pybs.unordered_tree.unordered_trees.Trees

   .. automethod:: Trees.index
   .. automethod:: Trees.non_superfluous_index

.. autoclass:: pybs.unordered_tree.unordered_trees.TreeOrder(order, tree_type)

   .. automethod:: TreeOrder.trees

   .. automethod:: TreeOrder.free_trees

   .. automethod:: TreeOrder.non_superfluous_trees

   .. automethod:: TreeOrder.number_of_free_trees_up_to_order

   .. automethod:: TreeOrder.number_of_non_superfluous_trees_up_to_order

   .. automethod:: TreeOrder.index

   .. automethod:: TreeOrder.non_superfluous_index

   .. automethod:: TreeOrder.tree_with_index

   .. automethod:: TreeOrder.free_tree_with_index

   .. automethod:: TreeOrder.non_superfluous_tree_with_index

.. autofunction:: tree_generator()

.. .. autofunction:: _ordinary_tree_generator
.. .. autofunction:: trees_of_order(order, sort=False, tree_type)
.. .. autofunction:: _graft_leaf_on_set

.. autofunction:: _graft_leaf

.. autofunction:: partition_into_free_trees


.. currentmodule:: pybs.unordered_tree.functions

.. autofunction:: number_of_trees_of_order(n)

.. autofunction:: number_of_trees_up_to_order

.. autofunction:: number_of_tree_pairs_of_total_order

