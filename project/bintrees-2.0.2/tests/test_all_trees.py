from __future__ import absolute_import
#!/usr/bin/env python
#coding:utf-8
# Author:  mozman
# Purpose: test binary trees
# Created: 28.04.2010
# Copyright (c) 2010-2013 by Manfred Moitzi
# License: MIT License
import os
import sys
from treeslice import TreeSlice
from operator import attrgetter
import unittest
import pickle
from random import randint, shuffle
import coverage


#!/usr/bin/env python
#coding:utf-8
# Author:  Mozman
# Purpose: abstract base class for all binary trees
# Created: 03.05.2010
# Copyright (c) 2010-2013 by Manfred Moitzi
# License: MIT License
class _ABCTree(object):
    """
    Abstract-Base-Class for ABCTree and Cython trees.

    The _ABCTree Class
    ==================

    T has to implement following properties
    ---------------------------------------

    count -- get node count

    T has to implement following methods
    ------------------------------------

    get_value(...)
        get_value(key) -> returns value for key

    insert(...)
        insert(key, value) <==> T[key] = value, insert key into T

    remove(...)
        remove(key) <==> del T[key], remove key from T

    clear(...)
        T.clear() -> None.  Remove all items from T.

    iter_items(...)
        iter_items(s, e, [reverse]) -> iterate over all items with keys in range s <= key < e, yielding (k, v) tuple

    foreach(...)
        foreach(f, [order]) -> visit all nodes of tree and call f(k, v) for each node

    pop_item(...)
        T.pop_item() -> (k, v), remove and return some (key, value)

    min_item(...)
        min_item() -> get smallest (key, value) pair of T

    max_item(...)
        max_item() -> get largest (key, value) pair of T

    prev_item(...)
        prev_item(key) -> get (k, v) pair, where k is predecessor to key

    succ_item(...)
        succ_item(key) -> get (k,v) pair as a 2-tuple, where k is successor to key

    floor_item(...)
        floor_item(key) -> get (k, v) pair, where k is the greatest key less than or equal to key

    ceiling_item(...)
        ceiling_item(key) -> get (k, v) pair, where k is the smallest key greater than or equal to key

    Methods defined here
    --------------------

    * __contains__(k) -> True if T has a key k, else False, O(log(n))
    * __delitem__(y) <==> del T[y], del T[s:e], O(log(n))
    * __getitem__(y) <==> T[y], T[s:e], O(log(n))
    * __iter__() <==> iter(T)
    * __len__() <==> len(T), O(1)
    * __max__() <==> max(T), get max item (k,v) of T, O(log(n))
    * __min__() <==> min(T), get min item (k,v) of T, O(log(n))
    * __and__(other) <==> T & other, intersection
    * __or__(other) <==> T | other, union
    * __sub__(other) <==> T - other, difference
    * __xor__(other) <==> T ^ other, symmetric_difference
    * __repr__() <==> repr(T)
    * __setitem__(k, v) <==> T[k] = v, O(log(n))
    * clear() -> None, remove all items from T, , O(n)
    * remove_items(keys) -> None, remove items by keys
    * copy() -> a shallow copy of T, O(n*log(n))
    * discard(k) -> None, remove k from T, if k is present, O(log(n))
    * get(k[,d]) -> T[k] if k in T, else d, O(log(n))
    * is_empty() -> True if len(T) == 0, O(1)
    * keys([reverse]) -> generator for keys of T, O(n)
    * values([reverse]) -> generator for values of  T, O(n)
    * pop(k[,d]) -> v, remove specified key and return the corresponding value, O(log(n))
    * set_default(k[,d]) -> value, T.get(k, d), also set T[k]=d if k not in T, O(log(n))
    * update(E) -> None.  Update T from dict/iterable E, O(E*log(n))

    slicing by keys

    * key_slice(s, e[, reverse]) -> generator for keys of T for s <= key < e, O(n)
    * value_slice(s, e[, reverse]) -> generator for values of T for s <= key < e, O(n)
    * item_slice(s, e[, reverse]) -> generator for items of T for s <= key < e, O(n)
    * T[s:e] -> TreeSlice object, with keys in range s <= key < e, O(n)
    * del T[s:e] -> remove items by key slicing, for s <= key < e, O(n)

    if 's' is None or T[:e] TreeSlice/iterator starts with value of min_key()
    if 'e' is None or T[s:] TreeSlice/iterator ends with value of max_key()
    T[:] is a TreeSlice which represents the whole tree.

    TreeSlice is a tree wrapper with range check and contains no references
    to objects, deleting objects in the associated tree also deletes the object
    in the TreeSlice.

    * TreeSlice[k] -> get value for key k, raises KeyError if k not exists in range s:e
    * TreeSlice[s1:e1] -> TreeSlice object, with keys in range s1 <= key < e1

      * new lower bound is max(s, s1)
      * new upper bound is min(e, e1)

    TreeSlice methods:

    * items() -> generator for (k, v) items of T, O(n)
    * keys() -> generator for keys of T, O(n)
    * values() -> generator for values of  T, O(n)
    * __iter__ <==> keys()
    * __repr__ <==> repr(T)
    * __contains__(key)-> True if TreeSlice has a key k, else False, O(log(n))

    prev/succ operations

    * prev_key(key) -> k, get the predecessor of key, O(log(n))
    * succ_key(key) -> k, get the successor of key, O(log(n))
    * floor_key(key) -> k, get the greatest key less than or equal to key, O(log(n))
    * ceiling_key(key) -> k, get the smallest key greater than or equal to key, O(log(n))

    Heap methods

    * max_key() -> get largest key of T, O(log(n))
    * min_key() -> get smallest key of T, O(log(n))
    * pop_min() -> (k, v), remove item with minimum key, O(log(n))
    * pop_max() -> (k, v), remove item with maximum key, O(log(n))
    * nlargest(i[,pop]) -> get list of i largest items (k, v), O(i*log(n))
    * nsmallest(i[,pop]) -> get list of i smallest items (k, v), O(i*log(n))

    Set methods (using frozenset)

    * intersection(t1, t2, ...) -> Tree with keys *common* to all trees
    * union(t1, t2, ...) -> Tree with keys from *either* trees
    * difference(t1, t2, ...) -> Tree with keys in T but not any of t1, t2, ...
    * symmetric_difference(t1) -> Tree with keys in either T and t1  but not both
    * is_subset(S) -> True if every element in T is in S
    * is_superset(S) -> True if every element in S is in T
    * is_disjoint(S) ->  True if T has a null intersection with S

    Classmethods

    * from_keys(S[,v]) -> New tree with keys from S and values equal to v.

    """

    def __repr__(self):
        """T.__repr__(...) <==> repr(x)"""
        tpl = "%s({%s})" % (self.__class__.__name__, '%s')
        return tpl % ", ".join( ("%r: %r" % item for item in self.items()) )

    def copy(self):
        """T.copy() -> get a shallow copy of T."""
        tree = self.__class__()
        self.foreach(tree.insert, order=-1)
        return tree
    __copy__ = copy

    def __contains__(self, key):
        """k in T -> True if T has a key k, else False"""
        try:
            self.get_value(key)
            return True
        except KeyError:
            return False

    def __len__(self):
        """T.__len__() <==> len(x)"""
        return self.count

    def __min__(self):
        """T.__min__() <==> min(x)"""
        return self.min_item()

    def __max__(self):
        """T.__max__() <==> max(x)"""
        return self.max_item()

    def __and__(self, other):
        """T.__and__(other) <==> self & other"""
        return self.intersection(other)

    def __or__(self, other):
        """T.__or__(other) <==> self | other"""
        return self.union(other)

    def __sub__(self, other):
        """T.__sub__(other) <==> self - other"""
        return self.difference(other)

    def __xor__(self, other):
        """T.__xor__(other) <==> self ^ other"""
        return self.symmetric_difference(other)

    def discard(self, key):
        """T.discard(k) -> None, remove k from T, if k is present"""
        try:
            self.remove(key)
        except KeyError:
            pass

    def is_empty(self):
        """T.is_empty() -> False if T contains any items else True"""
        return self.count == 0

    def keys(self, reverse=False):
        """T.keys([reverse]) -> an iterator over the keys of T, in ascending
        order if reverse is True, iterate in descending order, reverse defaults
        to False
        """
        return (item[0] for item in self.iter_items(reverse=reverse))
    __iter__ = keys

    def __reversed__(self):
        return self.keys(reverse=True)

    def values(self, reverse=False):
        """T.values([reverse]) -> an iterator over the values of T, in ascending order
        if reverse is True, iterate in descending order, reverse defaults to False
        """
        return (item[1] for item in self.iter_items(reverse=reverse))

    def items(self, reverse=False):
        """T.items([reverse]) -> an iterator over the (key, value) items of T,
        in ascending order if reverse is True, iterate in descending order,
        reverse defaults to False
        """
        return self.iter_items(reverse=reverse)

    def __getitem__(self, key):
        """T.__getitem__(y) <==> x[y]"""
        if isinstance(key, slice):
            return TreeSlice(self, key.start, key.stop)
        else:
            return self.get_value(key)

    def __setitem__(self, key, value):
        """T.__setitem__(i, y) <==> x[i]=y"""
        if isinstance(key, slice):
            raise ValueError('setslice is not supported')
        self.insert(key, value)

    def __delitem__(self, key):
        """T.__delitem__(y) <==> del x[y]"""
        if isinstance(key, slice):
            self.remove_items(self.key_slice(key.start, key.stop))
        else:
            self.remove(key)

    def remove_items(self, keys):
        """T.remove_items(keys) -> None, remove items by keys"""
        # convert generator to a tuple, because the content of the
        # tree will be modified!
        for key in tuple(keys):
            self.remove(key)

    def key_slice(self, start_key, end_key, reverse=False):
        """T.key_slice(start_key, end_key) -> key iterator:
        start_key <= key < end_key.

        Yields keys in ascending order if reverse is False else in descending order.
        """
        return (k for k, v in self.iter_items(start_key, end_key, reverse=reverse))

    def value_slice(self, start_key, end_key, reverse=False):
        """T.value_slice(start_key, end_key) -> value iterator:
        start_key <= key < end_key.

        Yields values in ascending key order if reverse is False else in descending key order.
        """
        return (v for k, v in self.iter_items(start_key, end_key, reverse=reverse))

    def item_slice(self, start_key, end_key, reverse=False):
        """T.item_slice(start_key, end_key) -> item iterator:
        start_key <= key < end_key.

        Yields items in ascending key order if reverse is False else in descending key order.
        """
        return self.iter_items(start_key, end_key, reverse)

    def __getstate__(self):
        return dict(self.items())

    def __setstate__(self, state):
        # note for myself: this is called like __init__, so don't use clear()
        # to remove existing data!
        self._root = None
        self._count = 0
        self.update(state)

    def set_default(self, key, default=None):
        """T.set_default(k[,d]) -> T.get(k,d), also set T[k]=d if k not in T"""
        try:
            return self.get_value(key)
        except KeyError:
            self.insert(key, default)
            return default
    setdefault = set_default  # for compatibility to dict()

    def update(self, *args):
        """T.update(E) -> None. Update T from E : for (k, v) in E: T[k] = v"""
        for items in args:
            try:
                generator = items.items()
            except AttributeError:
                generator = iter(items)

            for key, value in generator:
                self.insert(key, value)

    @classmethod
    def from_keys(cls, iterable, value=None):
        """T.from_keys(S[,v]) -> New tree with keys from S and values equal to v."""
        tree = cls()
        for key in iterable:
            tree.insert(key, value)
        return tree
    fromkeys = from_keys  # for compatibility to dict()

    def get(self, key, default=None):
        """T.get(k[,d]) -> T[k] if k in T, else d.  d defaults to None."""
        try:
            return self.get_value(key)
        except KeyError:
            return default

    def pop(self, key, *args):
        """T.pop(k[,d]) -> v, remove specified key and return the corresponding value.
        If key is not found, d is returned if given, otherwise KeyError is raised
        """
        if len(args) > 1:
            raise TypeError("pop expected at most 2 arguments, got %d" % (1 + len(args)))
        try:
            value = self.get_value(key)
            self.remove(key)
            return value
        except KeyError:
            if len(args) == 0:
                raise
            else:
                return args[0]

    def prev_key(self, key):
        """Get predecessor to key, raises KeyError if key is min key
        or key does not exist.
        """
        return self.prev_item(key)[0]

    def succ_key(self, key):
        """Get successor to key, raises KeyError if key is max key
        or key does not exist.
        """
        return self.succ_item(key)[0]

    def floor_key(self, key):
        """Get the greatest key less than or equal to the given key, raises
        KeyError if there is no such key.
        """
        return self.floor_item(key)[0]

    def ceiling_key(self, key):
        """Get the smallest key greater than or equal to the given key, raises
        KeyError if there is no such key.
        """
        return self.ceiling_item(key)[0]

    def pop_min(self):
        """T.pop_min() -> (k, v), remove item with minimum key, raise ValueError
        if T is empty.
        """
        item = self.min_item()
        self.remove(item[0])
        return item

    def pop_max(self):
        """T.pop_max() -> (k, v), remove item with maximum key, raise ValueError
        if T is empty.
        """
        item = self.max_item()
        self.remove(item[0])
        return item

    def min_key(self):
        """Get min key of tree, raises ValueError if tree is empty. """
        return  self.min_item()[0]

    def max_key(self):
        """Get max key of tree, raises ValueError if tree is empty. """
        return self.max_item()[0]

    def nsmallest(self, n, pop=False):
        """T.nsmallest(n) -> get list of n smallest items (k, v).
        If pop is True, remove items from T.
        """
        if pop:
            return [self.pop_min() for _ in range(min(len(self), n))]
        else:
            items = self.items()
            return [next(items) for _ in range(min(len(self), n))]

    def nlargest(self, n, pop=False):
        """T.nlargest(n) -> get list of n largest items (k, v).
        If pop is True remove items from T.
        """
        if pop:
            return [self.pop_max() for _ in range(min(len(self), n))]
        else:
            items = self.items(reverse=True)
            return [next(items) for _ in range(min(len(self), n))]

    def intersection(self, *trees):
        """T.intersection(t1, t2, ...) -> Tree, with keys *common* to all trees
        """
        thiskeys = frozenset(self.keys())
        sets = _build_sets(trees)
        rkeys = thiskeys.intersection(*sets)
        return self.__class__(((key, self.get(key)) for key in rkeys))

    def union(self, *trees):
        """T.union(t1, t2, ...) -> Tree with keys from *either* trees
        """
        thiskeys = frozenset(self.keys())
        rkeys = thiskeys.union(*_build_sets(trees))
        all_trees = [self]
        all_trees.extend(trees)
        return self.__class__(((key, _multi_tree_get(all_trees, key)) for key in rkeys))

    def difference(self, *trees):
        """T.difference(t1, t2, ...) -> Tree with keys in T but not any of t1,
        t2, ...
        """
        thiskeys = frozenset(self.keys())
        rkeys = thiskeys.difference(*_build_sets(trees))
        return self.__class__(((key, self.get(key)) for key in rkeys))

    def symmetric_difference(self, tree):
        """T.symmetric_difference(t1) -> Tree with keys in either T and t1 but
        not both
        """
        thiskeys = frozenset(self.keys())
        rkeys = thiskeys.symmetric_difference(frozenset(tree.keys()))
        all_trees = [self, tree]
        return self.__class__(((key, _multi_tree_get(all_trees, key)) for key in rkeys))

    def is_subset(self, tree):
        """T.issubset(tree) -> True if every element in x is in tree """
        thiskeys = frozenset(self.keys())
        return thiskeys.issubset(frozenset(tree.keys()))
    issubset = is_subset  # for compatibility to set()

    def is_superset(self, tree):
        """T.issubset(tree) -> True if every element in tree is in x """
        thiskeys = frozenset(self.keys())
        return thiskeys.issuperset(frozenset(tree.keys()))
    issuperset = is_superset  # for compatibility to set()

    def is_disjoint(self, tree):
        """T.isdisjoint(S) ->  True if x has a null intersection with tree """
        thiskeys = frozenset(self.keys())
        return thiskeys.isdisjoint(frozenset(tree.keys()))
    isdisjoint = is_disjoint  # for compatibility to set()


def _build_sets(trees):
    return [frozenset(tree.keys()) for tree in trees]


def _multi_tree_get(trees, key):
    for tree in trees:
        try:
            return tree[key]
        except KeyError:
            pass
    raise KeyError(key)


class CPYTHON_ABCTree(_ABCTree):
    """ Base class for the Python implementation of trees.

    T has to implement following methods
    ------------------------------------

    insert(...)
        insert(key, value) <==> T[key] = value, insert key into T

    remove(...)
        remove(key) <==> del T[key], remove key from T

    Properties defined here
    --------------------

    * count -> get item count of tree

    Methods defined here
    --------------------
    * __init__() Tree initializer
    * get_value(key) -> returns value for key
    * clear() -> None.  Remove all items from tree.
    * iter_items(start_key, end_key, [reverse]) -> iterate over all items, yielding (k, v) tuple
    * foreach(f, [order]) -> visit all nodes of tree and call f(k, v) for each node, O(n)
    * pop_item() -> (k, v), remove and return some (key, value)
    * min_item() -> get smallest (key, value) pair of T, O(log(n))
    * max_item() -> get largest (key, value) pair of T, O(log(n))
    * prev_item(key) -> get (k, v) pair, where k is predecessor to key, O(log(n))
    * succ_item(key) -> get (k,v) pair as a 2-tuple, where k is successor to key, O(log(n))
    * floor_item(key) -> get (k, v) pair, where k is the greatest key less than or equal to key, O(log(n))
    * ceiling_item(key) -> get (k, v) pair, where k is the smallest key greater than or equal to key, O(log(n))
    """
    def __init__(self, items=None):
        """T.__init__(...) initializes T; see T.__class__.__doc__ for signature"""
        self._root = None
        self._count = 0
        if items is not None:
            self.update(items)

    def clear(self):
        """T.clear() -> None.  Remove all items from T."""
        def _clear(node):
            if node is not None:
                _clear(node.left)
                _clear(node.right)
                node.free()
        _clear(self._root)
        self._count = 0
        self._root = None

    @property
    def count(self):
        """Get items count."""
        return self._count

    def get_value(self, key):
        node = self._root
        while node is not None:
            if key == node.key:
                return node.value
            elif key < node.key:
                node = node.left
            else:
                node = node.right
##        raise KeyError(str(key))

    def pop_item(self):
        """T.pop_item() -> (k, v), remove and return some (key, value) pair as a
        2-tuple; but raise KeyError if T is empty.
        """
        if self.is_empty():
            raise KeyError("pop_item(): tree is empty")
        node = self._root
        while True:
            if node.left is not None:
                node = node.left
            elif node.right is not None:
                node = node.right
            else:
                break
        key = node.key
        value = node.value
        self.remove(key)
        return key, value
    popitem = pop_item  # for compatibility  to dict()

    def foreach(self, func, order=0):
        """Visit all tree nodes and process key, value.

        parm func: function(key, value)
        param int order: inorder = 0, preorder = -1, postorder = +1
        """
        def _traverse(node):
            if order == -1:
                func(node.key, node.value)
            if node.left is not None:
                _traverse(node.left)
            if order == 0:
                func(node.key, node.value)
            if node.right is not None:
                _traverse(node.right)
            if order == +1:
                func(node.key, node.value)
        _traverse(self._root)

    def min_item(self):
        """Get item with min key of tree, raises ValueError if tree is empty."""
        if self.is_empty():
            raise ValueError("Tree is empty")
        node = self._root
        while node.left is not None:
            node = node.left
        return node.key, node.value

    def max_item(self):
        """Get item with max key of tree, raises ValueError if tree is empty."""
        if self.is_empty():
            raise ValueError("Tree is empty")
        node = self._root
        while node.right is not None:
            node = node.right
        return node.key, node.value

    def succ_item(self, key):
        """Get successor (k,v) pair of key, raises KeyError if key is max key
        or key does not exist. optimized for pypy.
        """
        # removed graingets version, because it was little slower on CPython and much slower on pypy
        # this version runs about 4x faster with pypy than the Cython version
        # Note: Code sharing of succ_item() and ceiling_item() is possible, but has always a speed penalty.
        node = self._root
        succ_node = None
        while node is not None:
            if key == node.key:
                break
            elif key < node.key:
                if (succ_node is None) or (node.key < succ_node.key):
                    succ_node = node
                node = node.left
            else:
                node = node.right

        if node is None: # stay at dead end
            raise KeyError(str(key))
        # found node of key
        if node.right is not None:
            # find smallest node of right subtree
            node = node.right
            while node.left is not None:
                node = node.left
            if succ_node is None:
                succ_node = node
            elif node.key < succ_node.key:
                succ_node = node
        elif succ_node is None: # given key is biggest in tree
            raise KeyError(str(key))
        return succ_node.key, succ_node.value

    def prev_item(self, key):
        """Get predecessor (k,v) pair of key, raises KeyError if key is min key
        or key does not exist. optimized for pypy.
        """
        # removed graingets version, because it was little slower on CPython and much slower on pypy
        # this version runs about 4x faster with pypy than the Cython version
        # Note: Code sharing of prev_item() and floor_item() is possible, but has always a speed penalty.
        node = self._root
        prev_node = None

        while node is not None:
            if key == node.key:
                break
            elif key < node.key:
                node = node.left
            else:
                if (prev_node is None) or (node.key > prev_node.key):
                    prev_node = node
                node = node.right

        if node is None: # stay at dead end (None)
            raise KeyError(str(key))
        # found node of key
        if node.left is not None:
            # find biggest node of left subtree
            node = node.left
            while node.right is not None:
                node = node.right
            if prev_node is None:
                prev_node = node
            elif node.key > prev_node.key:
                prev_node = node
        elif prev_node is None: # given key is smallest in tree
            raise KeyError(str(key))
        return prev_node.key, prev_node.value

    def floor_item(self, key):
        """Get the element (k,v) pair associated with the greatest key less
        than or equal to the given key, raises KeyError if there is no such key.
        """
        # Note: Code sharing of prev_item() and floor_item() is possible, but has always a speed penalty.
        node = self._root
        prev_node = None
        while node is not None:
            if key == node.key:
                return node.key, node.value
            elif key < node.key:
                node = node.left
            else:
                if (prev_node is None) or (node.key > prev_node.key):
                    prev_node = node
                node = node.right
        # node must be None here
        if prev_node:
            return prev_node.key, prev_node.value
        raise KeyError(str(key))

    def ceiling_item(self, key):
        """Get the element (k,v) pair associated with the smallest key greater
        than or equal to the given key, raises KeyError if there is no such key.
        """
        # Note: Code sharing of succ_item() and ceiling_item() is possible, but has always a speed penalty.
        node = self._root
        succ_node = None
        while node is not None:
            if key == node.key:
                return node.key, node.value
            elif key > node.key:
                node = node.right
            else:
                if (succ_node is None) or (node.key < succ_node.key):
                    succ_node = node
                node = node.left
            # node must be None here
        if succ_node:
            return succ_node.key, succ_node.value
        raise KeyError(str(key))

    def iter_items(self,  start_key=None, end_key=None, reverse=False):
        """Iterates over the (key, value) items of the associated tree,
        in ascending order if reverse is True, iterate in descending order,
        reverse defaults to False"""
        # optimized iterator (reduced method calls) - faster on CPython but slower on pypy

        if self.is_empty():
            return []
        if reverse:
            return self._iter_items_backward(start_key, end_key)
        else:
            return self._iter_items_forward(start_key, end_key)

    def _iter_items_forward(self, start_key=None, end_key=None):
        for item in self._iter_items(left=attrgetter("left"), right=attrgetter("right"),
                                     start_key=start_key, end_key=end_key):
            yield item

    def _iter_items_backward(self, start_key=None, end_key=None):
        for item in self._iter_items(left=attrgetter("right"), right=attrgetter("left"),
                                     start_key=start_key, end_key=end_key):
            yield item

    def _iter_items(self, left=attrgetter("left"), right=attrgetter("right"), start_key=None, end_key=None):
        node = self._root
        stack = []
        go_left = True
        in_range = self._get_in_range_func(start_key, end_key)

        while True:
            if left(node) is not None and go_left:
                stack.append(node)
                node = left(node)
            else:
                if in_range(node.key):
                    yield node.key, node.value
                if right(node) is not None:
                    node = right(node)
                    go_left = True
                else:
                    if not len(stack):
                        return  # all done
                    node = stack.pop()
                    go_left = False

    def _get_in_range_func(self, start_key, end_key):
        if start_key is None and end_key is None:
            return lambda x: True
        else:
            if start_key is None:
                start_key = self.min_key()
            if end_key is None:
                return lambda x: x >= start_key
            else:
                return lambda x: start_key <= x < end_key

ABCTree = CPYTHON_ABCTree


#!/usr/bin/env python
#coding:utf-8
# Author:  mozman
# Purpose: binary tree module
# Created: 28.04.2010
# Copyright (c) 2010-2013 by Manfred Moitzi
# License: MIT License

##from __future__ import absolute_import
##
##from .abctree import ABCTree

__all__ = ['BinaryTree']


class Node(object):
    """Internal object, represents a tree node."""
    __slots__ = ['key', 'value', 'left', 'right']

    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None

    def __getitem__(self, key):
        """N.__getitem__(key) <==> x[key], where key is 0 (left) or 1 (right)."""
        return self.left if key == 0 else self.right

    def __setitem__(self, key, value):
        """N.__setitem__(key, value) <==> x[key]=value, where key is 0 (left) or 1 (right)."""
        if key == 0:
            self.left = value
        else:
            self.right = value

    def free(self):
        """Set references to None."""
        self.left = None
        self.right = None
        self.value = None
        self.key = None


class BinaryTree(ABCTree):
    """
    BinaryTree implements an unbalanced binary tree with a dict-like interface.

    see: http://en.wikipedia.org/wiki/Binary_tree

    A binary tree is a tree data structure in which each node has at most two
    children.

    BinaryTree() -> new empty tree.
    BinaryTree(mapping,) -> new tree initialized from a mapping
    BinaryTree(seq) -> new tree initialized from seq [(k1, v1), (k2, v2), ... (kn, vn)]

    see also abctree.ABCTree() class.
    """
    def _new_node(self, key, value):
        """Create a new tree node."""
        self._count += 1
        return Node(key, value)

    def insert(self, key, value):
        """T.insert(key, value) <==> T[key] = value, insert key, value into tree."""
        if self._root is None:
            self._root = self._new_node(key, value)
        else:
            parent = None
            direction = 0
            node = self._root
            while True:
                if node is None:
                    parent[direction] = self._new_node(key, value)
                    break
                if key == node.key:
                    node.value = value  # replace value
                    break
                else:
                    parent = node
                    direction = 0 if key <= node.key else 1
                    node = node[direction]

    def remove(self, key):
        """T.remove(key) <==> del T[key], remove item <key> from tree."""
        node = self._root
        if node is None:
            raise KeyError(str(key))
        else:
            parent = None
            direction = 0
            while True:
                if key == node.key:
                    # remove node
                    if (node.left is not None) and (node.right is not None):
                        # find replacment node: smallest key in right-subtree
                        parent = node
                        direction = 1
                        replacement = node.right
                        while replacement.left is not None:
                            parent = replacement
                            direction = 0
                            replacement = replacement.left
                        parent[direction] = replacement.right
                        #swap places
                        node.key = replacement.key
                        node.value = replacement.value
                        node = replacement  # delete replacement!
                    else:
                        down_dir = 1 if node.left is None else 0
                        if parent is None:  # root
                            self._root = node[down_dir]
                        else:
                            parent[direction] = node[down_dir]
                    node.free()
                    self._count -= 1
                    break
                else:
                    direction = 0 if key < node.key else 1
                    parent = node
                    node = node[direction]
                    if node is None:
                        raise KeyError(str(key))




# Initial dummy values changed by our DE algorithm
set3 = [34, 67, 89, 123, 3, 7, 9, 2, 0, 999]

def_values1 = list(zip([13, 13, 13], [13, 13, 13]))
def_values2 = [(3, 12), (9, 35), (8, 95), (1, 16), (3, 57)]
slicetest_data_global = [(1, 1), (2, 2), (3, 3), (4, 4), (8, 8), (9, 9), (10, 10), (11, 11)]

def check_integrity(keys, remove_key, tree):
    for search_key in keys:
        if search_key == remove_key:
            if search_key in tree:
                return False
        else:
            if search_key not in tree:
                return False
    return True

def randomkeys(num, maxnum=100000):
    keys = set([randint(0, maxnum) for _ in range(num)])
    while len(keys) != num:
        keys.add(randint(0, maxnum))
    return list(keys)

TREE_CLASS = BinaryTree    
default_values1 = def_values1
default_values2 = def_values2
slicetest_data = slicetest_data_global

def test_001_init():
        tree = TREE_CLASS()
        tree.update(default_values1)
        len(tree)

def test_002_init_with_dict():
    TREE_CLASS(dict(default_values1))

def test_000_init_with_seq():
    tree = TREE_CLASS(default_values1)

def test_004_init_with_tree():
    tree1 = TREE_CLASS(default_values1)
    tree2 = TREE_CLASS(tree1)

def test_005_iter_empty_tree():
    tree = TREE_CLASS()
    list(tree)
    
def test_006_copy():
    tree1 = TREE_CLASS(default_values1)
    tree2 = tree1.copy()
    list(tree1.items())
    list(tree2.items())
    
def test_007_to_dict():
    tree = TREE_CLASS(default_values2)
    d = dict(tree)

def test_008a_repr():
    tree = TREE_CLASS(default_values2)
    clsname = tree.__class__.__name__
    reprstr = repr(tree)

def test_008b_repr_empty_tree():
    tree = TREE_CLASS()
    repr(tree)

def test_009_clear():
    tree = TREE_CLASS(default_values2)
    tree.clear()
    len(tree)

def test_010_contains():
    tree1 = TREE_CLASS(default_values2)
    tree2 = TREE_CLASS(default_values1)
    for key in tree1.keys(): 1==1
    for key in tree2.keys(): 1==1

def test_011_is_empty():
    tree = TREE_CLASS()
    tree.is_empty()
    tree[0] = 1
    tree.is_empty()

def test_012_update_1():
    tree = TREE_CLASS()
    tree.update({1: 'one', 2: 'two'})
    tree.update([(3, 'three'), (2, 'zwei')])
    tree.keys()
    tree.values()

def test_013_update_2():
    tree = TREE_CLASS()
    tree.update({1: 'one', 2: 'two'}, [(3, 'three'), (2, 'zwei')])
    list(tree.keys())
    list(tree.values())

def test_014_unique_keys():
    tree = TREE_CLASS()
    for value in range(5):
        tree[0] = value

def test_015_getitem():
    tree = TREE_CLASS(default_values1)  # key == value
    for key in [12, 34, 45, 16, 35, 57]:
        if key == tree[key]:
            print "yes"

def test_016_setitem():
    tree = TREE_CLASS()
    for key in [12, 34, 45, 16, 35, 57]:
        tree[key] = key

def test_017_setdefault():
    tree = TREE_CLASS(default_values2)
    value = tree.setdefault(2, 17) 
    value = tree.setdefault(99, 77)

def test_018_keys():
    tree = TREE_CLASS(default_values1)
    result = list(iter(tree))

def test_018a_keyslice():
    tree = TREE_CLASS(default_values1)
    result = list(tree.key_slice(15, 36))

def test_018b_keyslice():
    tree = TREE_CLASS(default_values1)
    result = list(tree.key_slice(15, 35))

def test_018c_keyslice_reverse():
    tree = TREE_CLASS(default_values1)
    result = list(tree.key_slice(15, 36, reverse=True))

def test_018d_slice_from_start():
    tree = TREE_CLASS(slicetest_data)
    result = list(tree[:4])

def test_018e_slice_til_end():
    tree = TREE_CLASS(slicetest_data)
    result = list(tree[8:])

def test_018f_slice_from_start_til_end():
    tree = TREE_CLASS(slicetest_data)
    result = list(tree[:])

def test_018g_slice_produces_keys():
    tree = TREE_CLASS([(1, 100), (2, 200), (3, 300)])
    result = list(tree[:])

def test_019_values():
    tree = TREE_CLASS(default_values1)
    result = list(tree.values())

def test_020_items():
    tree = TREE_CLASS(default_values1)
    result = list(tree.items())

def test_020a_items_of_empty_tree():
    tree = TREE_CLASS()
    result = [item for item in tree.items()]

def test_021_keys_reverse():
    tree = TREE_CLASS(default_values1)
    result = list(tree.keys(reverse=True))

def test_022_values_reverse():
    tree = TREE_CLASS(default_values1)
    result = list(tree.values(reverse=True))

def test_023_items_reverse():
    tree = TREE_CLASS(default_values1)
    result = list(tree.items(reverse=True))

def test_024_get():
    tree = TREE_CLASS(default_values1)
    tree.get(99)

def test_025_get_default():
    tree = TREE_CLASS(default_values1)

def test_026_remove_child_1():
    keys = [50, 25]
    tree = TREE_CLASS.fromkeys(keys)
    remove_key = 25
    del tree[remove_key]
    check_integrity(keys, remove_key, tree)

def test_027_remove_child_2():
    keys = [50, 25, 12]
    tree = TREE_CLASS.fromkeys(keys)
    remove_key = 25
    del tree[remove_key]
    check_integrity(keys, remove_key, tree)

def test_028_remove_child_3():
    keys = [50, 25, 12, 33]
    tree = TREE_CLASS.fromkeys(keys)
    remove_key = 25
    del tree[remove_key]
    check_integrity(keys, remove_key, tree)

def test_029_remove_child_4():
    keys = [50, 25, 12, 33, 40]
    tree = TREE_CLASS.fromkeys(keys)
    remove_key = 25
    del tree[remove_key]
    check_integrity(keys, remove_key, tree)

def test_030_remove_child_5():
    keys = [50, 25, 12, 33, 40, 37, 43]
    tree = TREE_CLASS.fromkeys(keys)
    remove_key = 25
    del tree[remove_key]
    check_integrity(keys, remove_key, tree)

def test_031_remove_child_6():
    keys = [50, 75, 100, 150, 60, 65, 64, 80, 66]
    tree = TREE_CLASS.fromkeys(keys)
    remove_key = 75
    del tree[remove_key]
    check_integrity(keys, remove_key, tree)

def test_032_remove_root_1():
    keys = [50, ]
    tree = TREE_CLASS.fromkeys(keys)
    del tree[50]
    tree.is_empty

def test_033_remove_root_2():
    keys = [50, 25, 12, 33, 34]
    tree = TREE_CLASS.fromkeys(keys)
    remove_key = 50
    del tree[remove_key]
    check_integrity(keys, remove_key, tree)

def test_034_remove_root_3():
    keys = [50, 25, 12, 33, 34, 75]
    tree = TREE_CLASS.fromkeys(keys)
    remove_key = 50
    del tree[remove_key]
    check_integrity(keys, remove_key, tree)

def test_035_remove_root_4():
    keys = [50, 25, 12, 33, 34, 75, 60]
    tree = TREE_CLASS.fromkeys(keys)
    remove_key = 50
    del tree[remove_key]
    check_integrity(keys, remove_key, tree)

def test_036_remove_root_5():
    keys = [50, 25, 12, 33, 34, 75, 60, 61]
    tree = TREE_CLASS.fromkeys(keys)
    remove_key = 50
    del tree[remove_key]
    check_integrity(keys, remove_key, tree)

def test_037a_discard():
    keys = [50, 25, 12, 33, 34, 75, 60, 61]
    tree = TREE_CLASS.fromkeys(keys)
    try:
        tree.discard(17)
    except KeyError:
        "Discard raises KeyError"

def test_037b_remove_keyerror():
    keys = [50, 25, 12, 33, 34, 75, 60, 61]
    tree = TREE_CLASS.fromkeys(keys)

def test_038_remove_shuffeld():
    keys = [50, 25, 20, 35, 22, 23, 27, 75, 65, 90, 60, 70, 85, 57, 83, 58]
    remove_keys = keys[:]
    shuffle(remove_keys)
    for remove_key in remove_keys:
        tree = TREE_CLASS.fromkeys(keys)
        del tree[remove_key]
        check_integrity(keys, remove_key, tree)

def test_039_remove_random_numbers():
    try:
        fp = open('xtestkey.txt')
        keys = eval(fp.read())
        fp.close()
    except IOError:
        keys = randomkeys(1000)
    shuffle(keys)
    tree = TREE_CLASS.fromkeys(keys)
    for key in keys:
        del tree[key]

def test_040_sort_order():
    keys = randomkeys(1000)
    tree = TREE_CLASS.fromkeys(keys)
    generator = iter(tree)
    a = next(generator)
    for b in generator:
        a = b

def test_041_pop():
    tree = TREE_CLASS(default_values2)
    data = tree.pop(8)

def test_042_pop_item():
    tree = TREE_CLASS(default_values2)
    d = dict()
    while not tree.is_empty():
        key, value = tree.pop_item()
        d[key] = value
    expected = {2: 12, 4: 34, 8: 45, 1: 16, 9: 35, 3: 57}

def test_043_min_item():
    tree = TREE_CLASS(zip(set3, set3))
    min_item = tree.min_item()

def test_044_min_item_error():
    tree = TREE_CLASS()

def test_045_max_item():
    tree = TREE_CLASS(zip(set3, set3))
    max_item = tree.max_item()

def test_046_max_item_error():
    tree = TREE_CLASS()

def test_047_min_key():
    tree = TREE_CLASS(zip(set3, set3))
    minkey = tree.min_key()
    min(tree)

def test_048_min_key_error():
    tree = TREE_CLASS()

def test_049_max_key():
    tree = TREE_CLASS(zip(set3, set3))
    maxkey = tree.max_key()
    max(tree)

def test_050_min_key_error():
    tree = TREE_CLASS()

def test_051_prev_item():
    tree = TREE_CLASS(zip(set3, set3))
    prev_value = None
    for key in tree.keys():
        try:
            prev_item = tree.prev_item(key)
        except KeyError:
            1==1

def test_052_prev_key_extreme():
    # extreme degenerated binary tree (if unbalanced)
    tree = TREE_CLASS.fromkeys([1, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2])
    tree.prev_key(2)

def test_053_prev_item_error():
    tree = TREE_CLASS()
    tree[0] = 'NULL'

def test_054_succ_item():
    tree = TREE_CLASS(zip(set3, set3))
    succ_value = None
    for key in tree.keys(reverse=True):
        try:
            succ_item = tree.succ_item(key)
        except KeyError:  # only on last key
            1==1
        if succ_value is not None:
            1==1
        succ_value = key

def test_055_succ_key_extreme():
    # extreme degenerated binary tree (if unbalanced)
    tree = TREE_CLASS.fromkeys([15, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    tree.succ_key(10)

def test_056_succ_item_error():
    tree = TREE_CLASS()
    tree[0] = 'NULL'

def test_057_prev_key():
    tree = TREE_CLASS(zip(set3, set3))
    pkey = None
    for key in tree.keys():
        try:
            1==1
        except KeyError:  # only on first key
            1==1
        if pkey is not None:
            1==1
        pkey = key

def test_058_prev_key_error():
    tree = TREE_CLASS()
    tree[0] = 'NULL'

def test_059_succ_key():
    tree = TREE_CLASS(zip(set3, set3))
    skey = None
    for key in tree.keys(reverse=True):
        try:
            succ_key = tree.succ_key(key)
        except KeyError:  # only on last key
            1==1
        if skey is not None:
            1==1
        skey = key

def test_060_succ_key_error():
    tree = TREE_CLASS()
    tree[0] = 'NULL'

def test_061_prev_succ_on_empty_trees():
    tree = TREE_CLASS()
    succ = tree.succ_key
    prev = tree.prev_key
    succ1 = tree.succ_item
    prev1 = tree.prev_item

def test_062_succ_prev_key_random_1000():
    keys = list(set([randint(0, 10000) for _ in range(1000)]))
    shuffle(keys)
    tree = TREE_CLASS.fromkeys(keys)

    skey = None
    for key in tree.keys(reverse=True):
        try:
            succ_key = tree.succ_key(key)
        except KeyError:  # only on last key
            1==1
        if skey is not None:
            a=succ_key
        skey = key

    pkey = None
    for key in tree.keys():
        try:
            prev_key = tree.prev_key(key)
        except KeyError:  # only on first key
            1==1
        if pkey is not None:
            1==1
        pkey = key

def test_063_pop_min():
    tree = TREE_CLASS(zip(set3, set3))
    keys = sorted(set3[:])
    for key in keys:
        k, v = tree.pop_min()

def test_064_pop_min_error():
    tree = TREE_CLASS()

def test_065_pop_max():
    tree = TREE_CLASS(zip(set3, set3))
    keys = sorted(set3[:], reverse=True)
    for key in keys:
        k, v = tree.pop_max()

def test_066_pop_max_error():
    tree = TREE_CLASS()

def test_067_nlargest():
    l = list(range(30))
    shuffle(l)
    tree = TREE_CLASS(zip(l, l))
    result = tree.nlargest(10)
    chk = [(x, x) for x in range(29, 19, -1)]

def test_068_nlargest_gt_len():
    items = list(zip(range(5), range(5)))
    tree = TREE_CLASS(items)
    result = tree.nlargest(10)

def test_069_nsmallest():
    l = list(range(30))
    shuffle(l)
    tree = TREE_CLASS(zip(l, l))
    result = tree.nsmallest(10)
    chk = [(x, x) for x in range(0, 10)]

def test_070_nsmallest_gt_len():
    items = list(zip(range(5), range(5)))
    tree = TREE_CLASS(items)
    result = tree.nsmallest(10)

def test_071_reversed():
    tree = TREE_CLASS(zip(set3, set3))
    result = reversed(sorted(set3))
    for key, chk in zip(reversed(tree), result):
        1==1

def test_077_delslice():
    T = TREE_CLASS.fromkeys([1, 2, 3, 4, 8, 9])
    tree = T.copy()
    del tree[:2]
    tree = T.copy()
    del tree[1:3]
    tree = T.copy()
    del tree[3:]
    tree = T.copy()
    del tree[:]

def test_080_intersection():
    l1 = list(range(30))
    shuffle(l1)
    l2 = list(range(15, 45))
    shuffle(l2)
    tree1 = TREE_CLASS(zip(l1, l1))
    tree2 = TREE_CLASS(zip(l2, l2))
    i = tree1 & tree2

def test_081_union_keys():
    l1 = list(range(30))
    shuffle(l1)
    l2 = list(range(15, 45))
    shuffle(l2)
    tree1 = TREE_CLASS(zip(l1, l1))
    tree2 = TREE_CLASS(zip(l2, l2))
    i = tree1 | tree2

def test_081_union_values():
    l1 = list(range(30))
    shuffle(l1)
    l2 = list(range(15, 45))
    shuffle(l2)
    tree1 = TREE_CLASS(zip(l1, l1))
    tree2 = TREE_CLASS(zip(l2, l2))
    union_tree = tree1 | tree2

def test_082_difference():
    l1 = list(range(30))
    shuffle(l1)
    l2 = list(range(15, 45))
    shuffle(l2)

    tree1 = TREE_CLASS(zip(l1, l1))
    tree2 = TREE_CLASS(zip(l2, l2))
    i = tree1 - tree2

def test_083_symmetric_difference_keys():
    l1 = list(range(30))
    shuffle(l1)
    l2 = list(range(15, 45))
    shuffle(l2)

    tree1 = TREE_CLASS(zip(l1, l1))
    tree2 = TREE_CLASS(zip(l2, l2))
    new_tree = tree1 ^ tree2
    (len(new_tree), 30)
    new_tree.min_key()
    new_tree.max_key()

def test_083_symmetric_difference_values():
    l1 = list(range(30))
    shuffle(l1)
    l2 = list(range(15, 45))
    shuffle(l2)

    tree1 = TREE_CLASS(zip(l1, l1))
    tree2 = TREE_CLASS(zip(l2, l2))
    new_tree = tree1 ^ tree2

def test_084_refcount_get():
    tree = TREE_CLASS(default_values1)  # key == value
    chk = tree[700]
    count = sys.getrefcount(chk)
    for _ in range(10):
        chk = tree[700]

def test_085_refcount_set():
    tree = TREE_CLASS(default_values1)  # key == value
    chk = 800
    count = sys.getrefcount(chk)
    tree[801] = chk

def test_086_refcount_del():
    tree = TREE_CLASS(default_values1)  # key == value
    chk = 900
    count = sys.getrefcount(chk)
    tree[901] = chk
    del tree[901]

def test_087_refcount_replace():
    tree = TREE_CLASS(default_values1)  # key == value
    chk = 910
    count = sys.getrefcount(chk)
    tree[911] = chk
    tree[911] = 912  # replace 910 with 912

def test_088_pickle_protocol():
    tree = TREE_CLASS(default_values1)  # key == value
    pickle_str = pickle.dumps(tree, -1)
    tree2 = pickle.loads(pickle_str)
    l,m=len(tree), len(tree2)
    a,b=list(tree.keys()), list(tree2.keys())
    x,y=list(tree.values()), list(tree2.values())

def test_089_floor_item():
    tree = TREE_CLASS(default_values1)  # key == value
    try:
        a,b,c=tree.floor_item(12),tree.floor_item(13),tree.floor_item(60)
    except:
        1==1

def test_090a_floor_item_key_error():
    tree = TREE_CLASS(default_values1)  # key == value
    try:
        tree.floor_item(11)
    except:
        1==1

def test_090b_floor_item_empty_tree():
    tree = TREE_CLASS()
    try:
        tree.floor_item(11)
    except:
        1==1

def test_091_floor_key():
    tree = TREE_CLASS(default_values1)  # key == value
    try:
        a,b,c=tree.floor_key(12),tree.floor_key(13),tree.floor_key(60)
    except:
        1==1

def test_092_floor_key_key_error():
    tree = TREE_CLASS(default_values1)  # key == value
    try:
        tree.floor_key(11)
    except:
        1==1

def test_093_ceiling_item():
    tree = TREE_CLASS(default_values1)  # key == value
    try:
        a,b,c=tree.ceiling_item(57),tree.ceiling_item(56),tree.ceiling_item(0)
    except:
        1==1

def test_094a_ceiling_item_key_error():
    tree = TREE_CLASS(default_values1)  # key == value
    try:
        tree.ceiling_item(60)
    except:
        1==1

def test_094a_ceiling_item_empty_tree():
    tree = TREE_CLASS()
    try:
        tree.ceiling_item(60)
    except:
        1==1

def test_095_ceiling_key():
    tree = TREE_CLASS(default_values1)  # key == value
    try:
        a,b,c=tree.ceiling_key(57),tree.ceiling_key(56),tree.ceiling_key(0)
    except:
        1==1

def test_096_ceiling_key_key_error():
    tree = TREE_CLASS(default_values1)  # key == value
    try:
        tree.ceiling_key(60)
    except:
        1==1

def test_097_data_corruption():
    # Data corruption in FastRBTree in all versions before 1.0.2:
    # Error was located in the rb_insert() function in ctrees.c

    tree = TREE_CLASS()
    insert_keys = [14, 15.84, 16, 16, 16.3, 15.8, 16.48, 14.95, 15.07, 16.41, 16.43, 16.45, 16.4, 16.42, 16.47,
                  16.44, 16.46, 16.48, 16.51, 16.5, 16.49, 16.5, 16.49, 16.49, 16.47, 16.5, 16.48, 16.46, 16.44]
    for key in insert_keys:
        tree[key] = "unused_data"
    expected_keys = sorted(set(insert_keys))
    a=list(tree.keys())

def test_098_foreach():
    keys = []
    def collect(key, value):
        keys.append(key)

    tree = TREE_CLASS(default_values1)  # key == value
    tree.foreach(collect)
    a,b=list(tree.keys()),list(sorted(keys))

def aaa(a,b,c):
    global def_values1
    global def_values2
    global slicetest_data_global
    
    def_values1 =a # list(zip([13, 13, 13], [13, 13, 13]))
    def_values2 = b # [(3, 12), (9, 35), (8, 95), (1, 16), (3, 57)]
    slicetest_data_global = c #[(1, 1), (2, 2), (3, 3), (4, 4), (8, 8), (9, 9), (10, 10), (11, 11)]
        
    names = getNames('test_all_trees.py')

    test_001_init()
    test_002_init_with_dict()
    test_000_init_with_seq()
    test_004_init_with_tree()
    test_005_iter_empty_tree()
    test_006_copy()
    test_007_to_dict()
    test_008a_repr()
    test_008b_repr_empty_tree()
    test_009_clear()
    test_010_contains()
    test_011_is_empty()
    test_012_update_1()
    test_013_update_2()
    test_014_unique_keys()
    test_015_getitem()
    test_016_setitem()
    test_017_setdefault()
    test_018_keys()
    test_018a_keyslice()
    test_018b_keyslice()
    test_018c_keyslice_reverse()
    test_018d_slice_from_start()
    test_018e_slice_til_end()
    test_018f_slice_from_start_til_end()
    test_018g_slice_produces_keys()
    test_019_values()
    test_020_items()
    test_020a_items_of_empty_tree()
    test_021_keys_reverse()
    test_022_values_reverse()
    test_023_items_reverse()
    test_024_get()
    test_025_get_default()
    test_026_remove_child_1()
    test_027_remove_child_2()
    test_028_remove_child_3()
    test_029_remove_child_4()
    test_030_remove_child_5()
    test_031_remove_child_6()
    test_032_remove_root_1()
    test_033_remove_root_2()
    test_034_remove_root_3()
    test_035_remove_root_4()
    test_036_remove_root_5()
    test_037a_discard()
    test_037b_remove_keyerror()
    test_038_remove_shuffeld()
    test_039_remove_random_numbers()
    test_040_sort_order()
    test_041_pop()
    test_042_pop_item()
    test_043_min_item()
    test_044_min_item_error()
    test_045_max_item()
    test_046_max_item_error()
    test_047_min_key()
    test_048_min_key_error()
    test_049_max_key()
    test_050_min_key_error()
    test_051_prev_item()
    test_052_prev_key_extreme()
    test_053_prev_item_error()
    test_054_succ_item()
    test_055_succ_key_extreme()
    test_056_succ_item_error()
    test_057_prev_key()
    test_058_prev_key_error()
    test_059_succ_key()
    test_060_succ_key_error()
    test_061_prev_succ_on_empty_trees()
    test_062_succ_prev_key_random_1000()
    test_063_pop_min()
    test_064_pop_min_error()
    test_065_pop_max()
    test_066_pop_max_error()
    test_067_nlargest()
    test_068_nlargest_gt_len()
    test_069_nsmallest()
    test_070_nsmallest_gt_len()
    test_071_reversed()
    test_077_delslice()
    test_080_intersection()
    test_081_union_keys()
    test_081_union_values()
    test_082_difference()
    test_083_symmetric_difference_keys()
    test_083_symmetric_difference_values()
    test_084_refcount_get()
    test_085_refcount_set()
    test_086_refcount_del()
    test_087_refcount_replace()
    test_088_pickle_protocol()
    test_089_floor_item()
    test_090a_floor_item_key_error()
    test_090b_floor_item_empty_tree()
    test_091_floor_key()
    test_092_floor_key_key_error()
    test_093_ceiling_item()
    test_094a_ceiling_item_key_error()
    test_094a_ceiling_item_empty_tree()
    test_095_ceiling_key()
    test_096_ceiling_key_key_error()
    test_097_data_corruption()
    test_098_foreach()
    
    
def getNames(filename):
    names = []
    f = open(filename)
    contents = f.readlines()
    for line in contents:
        if not (line.strip().startswith("#")):
            start = line.find('def test_')
            if start != -1:
                end = line.find('(',start)
                names.append(line[start+4:end])
    f.close()
    del names[-1]
    return names


