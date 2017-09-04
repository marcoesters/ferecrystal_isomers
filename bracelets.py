"""
This module creates bracelets with fixed content according to
Karim, S.; Sawada, J.; Alambir; Z.; and Husnine, S. M. "Generating
bracelets with fixed content", Theor. Comput. Sci., 2013, 475,
103 - 112, DOI: 10.1016/j.tcs.2012.11.024
"""

from __future__ import division, unicode_literals, print_function
from string import ascii_uppercase

__author__ = "Marco Esters"
__copyright__ = "Copyright 2017, Marco Esters"
__version__ = "1.0"
__maintainer__ = "Marco Esters"
__email__ = "esters@uoregon.edu"
__date__ = "03/06/2017"


class Bracelets(object):

    """
    Object for the bracelets to be instantiated by the
    ferecrystal_isomer module.

    """

    def __init__(self, components):
        """
        Args:
           components (list or tuple): A list of integers representing
               the fixed content.
        """
        if not isinstance(components, list):
            raise TypeError("Components must be list.")
        if len(components) < 2:
            raise ValueError("Components must have at least 2 items.")

        self._components = components
        dll = DoubleLinkedList(self._components)
        self._bracelets = sorted(list(self.get_bracelets(dll)))

    def as_string(self):
        string_list = [''] * len(self.bracelets)
        for b, brace in enumerate(self.bracelets):
            for s in brace:
                string_list[b] += ascii_uppercase[s]
        return string_list

    def as_tuple(self):
        bracelet_tuple = []
        for brac in self.bracelets:
            tuple_list = []
            curr = 0
            n = 1
            for b in brac[1:]:
                if b == curr:
                    n += 1
                else:
                    tuple_list.append((curr, n))
                    curr = b
                    n = 1
            tuple_list.append((curr, n))
            bracelet_tuple.append(tuple_list)
        return bracelet_tuple

    @property
    def bracelets(self):
        return self._bracelets

    def build_bracelets(self, a, dll, lenenc, run, t, p, r, z, b, RS):
        if t - 1 > r + (dll.n_tot-r)/2:
            if a[t-2] > a[dll.n_tot-t+r+1]:
                RS = False
            elif a[t-2] < a[dll.n_tot-t+r+1]:
                RS = True

        if dll.n[-1] == dll.n_tot - t + 1:
            if dll.n[-1] > run[t-p-1]:
                p = dll.n_tot

            if dll.n[-1] > 0 and r + 1 != t:
                if lenenc[b+1][0] == dll.n_items - 1\
                      and lenenc[b+1][1] > dll.n[-1]:
                    RS = True

                elif (lenenc[b+1][0] != dll.n_items - 1
                      or lenenc[b+1][1] < dll.n[-1]):
                    RS = False

            if not RS and dll.n_tot == p:
                yield a

        elif dll.n[0] != dll.n_tot - t + 1:
            j = dll.head
            while j >= a[t-p-1]:
                run[z-1] = t - z
                lenenc = self.update_run_length(j, lenenc)
                dll.n[j] -= 1
                if dll.n[j] == 0:
                    dll.remove(j)

                a[t-1] = j
                z2 = z
                if j != dll.n_items - 1:
                    z2 = t + 1
                if j != a[t-p-1]:
                    p2 = t
                else:
                    p2 = p

                c = self.check_rev(lenenc)
                if c == 0:
                    for brac in self.build_bracelets(a[:], dll, lenenc,
                                                     run, t + 1, p2, t,
                                                     z2, lenenc[0], False):
                        yield brac

                elif c == 1:
                    for brac in self.build_bracelets(a[:], dll, lenenc,
                                                     run, t + 1, p2, r,
                                                     z2, b, RS):
                        yield brac

                if dll.n[j] == 0:
                    dll.add(j)
                dll.n[j] += 1
                lenenc = self.restore_run_length(lenenc)
                j = dll.next[j]

            a[t-1] = dll.n_tot - 1

    def check_rev(self, lenenc):
        i = 1
        m = lenenc[0]
        while lenenc[i] == lenenc[m-i+1] and i <= m/2:
            i += 1
        if i > m/2:
            return 0
        if lenenc[i][0] < lenenc[m-i+1][0]:
            return 1
        if lenenc[i][0] > lenenc[m-i+1][0]:
            return -1
        if ((lenenc[i][1] < lenenc[m-i+1][1]
             and lenenc[i+1][0] < lenenc[m-i+1])
            or (lenenc[i][1] > lenenc[m-i+1][1]
                and lenenc[i][0] < lenenc[m-i][0])):
            return 1
        return -1

    def get_bracelets(self, dll):
        run = [0] * dll.n_tot

        a = [dll.n_items - 1] * dll.n_tot
        a[0] = 0
        dll.n[0] -= 1
        lenenc = [1, [0, 1]]
        if dll.n[0] == 0:
            dll.remove(0)

        for brac in self.build_bracelets(a, dll, lenenc, run,
                                         2, 1, 1, 2, 1, False):
            yield brac

    def restore_run_length(self, lenenc):
        if lenenc[-1][1] == 1:
            lenenc[0] -= 1
            del lenenc[-1]
        else:
            lenenc[-1][1] -= 1

        return lenenc

    def update_run_length(self, j, lenenc):
        if lenenc[-1][0] == j:
            lenenc[-1][1] += 1
        else:
            lenenc[0] += 1
            lenenc.append([j, 1])

        return lenenc


class DoubleLinkedList(object):
    """
    Object for the double linked list to efficiently implement add
    and remove operations. See Karim's paper for details.

    """
    def __init__(self, component_list):
        """
        Generates the double linked list.

        Args:
            component_list (list or tuple): integer list representing
                the fixed content.
        """
        self.n = component_list[:]
        self.n_items = len(component_list)
        self.n_tot = sum(component_list)
        self.next = []
        self.prev = []
        for i in range(self.n_items+1):
            self.next.append(i-1)
            self.prev.append(i+1)
        self._head = self.n_items - 1

    def add(self, j):
        """
        The 'add(j)' operation as outlined in Karim's publication.
        """
        n = self.next[j]
        p = self.prev[j]
        self.prev[n] = j
        self.next[p] = j
        if self.prev[j] == self.n_items:
            self._head = j

    @property
    def head(self):
        """
        The 'head' operation as outlined in Karim's publication.
        """
        return self._head

    def remove(self, j):
        """
        The 'remove(j)' operation as outlined in Karim's publication.
        """
        if j == self._head:
            self._head = self.next[j]
        n = self.next[j]
        p = self.prev[j]
        self.next[p] = n
        self.prev[n] = p
