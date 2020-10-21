#!/usr/bin/env python3

class Node:
    """Node in a binary tree `Tree`"""

    def __init__(self, key, left=None, right=None, parent=None):
        self.key = key
        self.parent = parent
        self.left = left
        self.right = right
        if left is not None: left.parent = self
        if right is not None: right.parent = self

    def is_left_son(self):
        return self.parent.left is self

    def is_right_son(self):
        return self.parent.right is self
class Tree:
    """A simple binary search tree"""

    def __init__(self, root=None):
        self.root = root

    def rotate(self, node):
        """ Rotate the given `node` up.

        Performs a single rotation of the edge between the given node
        and its parent, choosing left or right rotation appropriately.
        """
        if node.parent is not None:
            if node.parent.left == node:
                if node.right is not None: node.right.parent = node.parent
                node.parent.left = node.right
                node.right = node.parent
            else:
                if node.left is not None: node.left.parent = node.parent
                node.parent.right = node.left
                node.left = node.parent
            if node.parent.parent is not None:
                if node.parent.parent.left == node.parent:
                    node.parent.parent.left = node
                else:
                    node.parent.parent.right = node
            else:
                self.root = node
            node.parent.parent, node.parent = node, node.parent.parent

    def lookup(self, key):
        """Look up the given key in the tree.

        Returns the node with the requested key or `None`.
        """
        if self.root is None:
            return None

        node = self.root
        while node is not None:
            last_visited = node

            if node.key == key:
                self.splay(node)
                return node

            if key < node.key:
                node = node.left
            else:
                node = node.right

        self.splay(last_visited)
        return None


    def insert(self, key):
        """Insert key into the tree.

        If the key is already present, nothing happens.
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
        self.splay(node)

    def remove(self, key):
        """Remove given key from the tree.

        It the key is not present, nothing happens.
        """
        if self.root is None:
            return

        node = self.root

        # find the node to delete
        while node is not None and node.key != key:
            last_visited = node
            if key < node.key:
                node = node.left
            else:
                node = node.right

        if node is not None:
            if node.left is not None and node.right is not None:
                replacement = node.right
                while replacement.left is not None:
                    replacement = replacement.left
                node.key = replacement.key
                node = replacement

            replacement = node.left if node.left is not None else node.right
            # replacement is not None iif the node being removed has exactly 1 son
            # node is pointing to the node that we want to remove
            if node.parent is not None:
                if node.parent.left == node: node.parent.left = replacement
                else: node.parent.right = replacement

            else:
                self.root = replacement
            if replacement is not None:
                replacement.parent = node.parent
                self.splay(replacement)
            elif node.parent is not None:
                self.splay(node.parent)
            
            
        else:
            # unsuccessful find
            self.splay(last_visited)
            


    def zig_zig(self, node):
        self.rotate(node.parent)
        self.rotate(node)

    def zig_zag(self, node):
        self.rotate(node)
        self.rotate(node)

    def splay(self, node):
        """Splay the given node.

        If a single rotation needs to be performed, perform it as the last rotation
        (i.e., to move the splayed node to the root of the tree).
        """

        # while splayed node isn't the root
        while node.parent is not None:

            # perform the last zig
            if node.parent.parent is None:
                self.rotate(node)

            elif (node.is_left_son() and node.parent.is_left_son()) or (node.is_right_son() and node.parent.is_right_son()):
                 self.zig_zig(node)
            else:
                self.zig_zag(node)
            
