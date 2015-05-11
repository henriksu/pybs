Trees
===========================

.. toctree::

   UnorderedTrees
   FreeTrees
   ToolsForTrees
 
This part deals with trees up to, but not including, forests, linear combinations of trees and grafting.

Note that the one vertex tree can be accessed as  ``pybs.unordered_tree.leaf``.
Importing this is more convenient and saves memory compared to writing ``UnoredredTree()``.

Also note that the :class:`Trees`-object ``pybs.unordered_tree.the_trees`` holds a pool of trees.
It is initiated on import and handles construction and memoization of rooted as well as free trees.
