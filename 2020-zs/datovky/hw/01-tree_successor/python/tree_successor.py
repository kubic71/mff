#!/usr/bin/env python3

class Node:
    """Node in a binary tree `Tree`"""

    def __init__(self, key, left=None, right=None, parent=None):
        self.key = key
        self.left = left
        self.right = right
        self.parent = parent

class Tree:
    """A simple binary search tree"""

    def __init__(self, root=None):
        self.root = root
        
    def insert(self, key):
        """Insert key into the tree.

        If the key is already present, do nothing.
        """
        if self.root is None:
            self.root = Node(key)
            return

        node = self.root
        while node.key != key:
            if key < node.key:
                if node.left is None:
                    node.left = Node(key, parent=node)
                node = node.left
            else:
                if node.right is None:
                    node.right = Node(key, parent=node)
                node = node.right
                
#    def _find_min(self, node):
#        # find min in subtree rooted at node
#        if node.left is None:
#            return node
#
#        return self._find_min(node.left)
                
    def _find_min(self, node):
        while node.left is not None:
            node = node.left
        return node
            

        

    def successor(self, node=None):
        """Return successor of the given node.

        The successor of a node is the node with the next greater key.
        Return None if there is no such node.
        If the argument is None, return the node with the smallest key.
        """

        if node is None:
            return self._find_min(self.root)
            

        # return minimum of right subtree, if it exist
        if node.right is not None:
            return self._find_min(node.right)
        
        # if node doesn't have right subtree, it is already a maximum in some subtree
        # the successor therefore is the parent node of this subtree

        while node.parent is not None:
            
            # if node is the left son of its parent 
            if node.parent.left is node:
                return node.parent
                
            node = node.parent
            
        return None