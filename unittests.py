import unittest
from bracelets import Bracelets, DoubleLinkedList
from copy import deepcopy
from ferecrystal_isomers import Isomers
from string import ascii_uppercase


class IsomerTest(unittest.TestCase):
    def setUp(self):
        self.composition = [3, 4, 5]
        self.elements = ['VSe2', 'SnSe', 'SnSe2']
        self.isomers = Isomers(self.composition, self.elements)
        self.isomers_no_el = Isomers(self.composition)

    def test_formula(self):
        formula = '(VSe2)3(SnSe)4(SnSe2)5'
        formula_no_el = '(A)3(B)4(C)5'
        self.assertEqual(self.isomers.get_formula(), formula)
        self.assertEqual(self.isomers_no_el.get_formula(), formula_no_el)

    def test_isomers(self):
        iso = ['(VSe2)1-(SnSe)2-(SnSe2)3',
               '(VSe2)1-(SnSe)1-(SnSe2)1-(SnSe)1-(SnSe2)2',
               '(VSe2)1-(SnSe)1-(SnSe2)2-(SnSe)1-(SnSe2)1',
               '(VSe2)1-(SnSe)1-(SnSe2)3-(SnSe)1',
               '(VSe2)1-(SnSe2)1-(SnSe)2-(SnSe2)2',
               '(VSe2)1-(SnSe2)1-(SnSe)1-(SnSe2)1-(SnSe)1-(SnSe2)1']
        self.assertEqual(iso, Isomers([1, 2, 3], self.elements).isomers)

    def test_thickness(self):
        thick4 = {'SnSe2': 4}
        sub4 = self.isomers.get_isomer_subset(thickness_conditions=thick4)
        thick5 = {'SnSe2': 5}
        sub5 = self.isomers.get_isomer_subset(thickness_conditions=thick5)
        thick45 = {'SnSe2': (4, 5)}
        sub45 = self.isomers.get_isomer_subset(thickness_conditions=thick45)
        self.assertEqual(len(sub4), 105)
        self.assertEqual(sub5, sub45)
        iso = ['(VSe2)3-(SnSe)2-(SnSe2)5-(SnSe)2',
               '(VSe2)2-(SnSe)2-(VSe2)1-(SnSe)2-(SnSe2)5',
               '(VSe2)2-(SnSe)2-(VSe2)1-(SnSe2)5-(SnSe)2',
               '(VSe2)1-(SnSe)2-(VSe2)1-(SnSe)2-(VSe2)1-(SnSe2)5']
        thick = {'SnSe': (2, 2), 'SnSe2': 5}
        sub = self.isomers.get_isomer_subset(thickness_conditions=thick)
        self.assertEqual(sub, iso)

    def test_interface(self):
        ifacf = {'VSe2SnSe': False}
        sub_false = self.isomers.get_isomer_subset(interface_conditions=ifacf)
        self.assertEqual(len(sub_false), 55)
        ifact = {'VSe2SnSe': True}
        sub_true = self.isomers.get_isomer_subset(interface_conditions=ifact)
        ifactup = {'VSe2SnSe': (1, 0)}
        sub_tup = self.isomers.get_isomer_subset(interface_conditions=ifactup)
        self.assertEqual(sub_tup, sub_true)
        iface = {'VSe2SnSe': (4, 5)}
        sub = self.isomers.get_isomer_subset(interface_conditions=iface)
        self.assertEqual(len(sub), 96)
        ifaci = {'VSe2SnSe': 5}
        sub_i = self.isomers.get_isomer_subset(interface_conditions=ifaci)
        ifact = {'VSe2SnSe': (5, 5)}
        sub_t = self.isomers.get_isomer_subset(interface_conditions=ifact)
        self.assertEqual(sub_i, sub_t)
        

class BraceletTest(unittest.TestCase):
    """
    Test class for the bracelets created with bracelets.py
    """
    def setUp(self):
        self.components = [1, 2, 3]
        self.bracelets = Bracelets(self.components)

    def test_bracelets(self):
        brac = [[0, 1, 1, 2, 2, 2],
                [0, 1, 2, 1, 2, 2],
                [0, 1, 2, 2, 1, 2],
                [0, 1, 2, 2, 2, 1],
                [0, 2, 1, 1, 2, 2],
                [0, 2, 1, 2, 1, 2]]
        self.assertIsInstance(self.bracelets.bracelets, list)
        self.assertEqual(len(self.bracelets.bracelets), 6)
        self.assertEqual(self.bracelets.bracelets, brac)

    def test_as_string(self):
        brac = ['ABBCCC', 'ABCBCC', 'ABCCBC', 'ABCCCB', 'ACBBCC', 'ACBCBC']
        self.assertIsInstance(self.bracelets.as_string()[0], basestring)
        self.assertEqual(self.bracelets.as_string(), brac)

    def test_as_tuple(self):
        brac = [[(0, 1), (1, 2), (2, 3)],
                [(0, 1), (1, 1), (2, 1), (1, 1), (2, 2)],
                [(0, 1), (1, 1), (2, 2), (1, 1), (2, 1)],
                [(0, 1), (1, 1), (2, 3), (1, 1)],
                [(0, 1), (2, 1), (1, 2), (2, 2)],
                [(0, 1), (2, 1), (1, 1), (2, 1), (1, 1), (2, 1)]]
        self.assertIsInstance(self.bracelets.as_tuple()[0][0], tuple)
        self.assertEqual(self.bracelets.as_tuple(), brac)


class DLLTest(unittest.TestCase):
    """
    Test class for the double-linked list used in bracelets.py
    """
    def setUp(self):
        self.components = [3, 4, 5]
        self.dll = DoubleLinkedList(self.components)

    def test_init(self):
        nxt = [i - 1 for i in range(len(self.components) + 1)]
        prv = [i + 1 for i in range(len(self.components) + 1)]
        self.assertEqual(self.dll.n, self.components)
        self.assertEqual(self.dll.n_items, len(self.components))
        self.assertEqual(self.dll.n_tot, sum(self.components))
        self.assertEqual(self.dll.next, nxt)
        self.assertEqual(self.dll.prev, prv)
        self.assertEqual(self.dll.head, nxt[-1])

    def test_add_remove(self):
        dll_add_rem = deepcopy(self.dll)
        dll_add_rem.remove(1)
        self.assertEqual(dll_add_rem.next, [-1, 0, 0, 2])
        self.assertEqual(dll_add_rem.prev, [2, 2, 3, 4])
        self.assertEqual(dll_add_rem.head, self.dll.head)
        dll_add_rem.add(1)
        self.assertEqual(dll_add_rem.next, self.dll.next)
        self.assertEqual(dll_add_rem.prev, self.dll.prev)
        # Removing the last item should change head, adding restores it
        dll_add_rem.remove(2)
        self.assertEqual(dll_add_rem.head, 1)
        dll_add_rem.add(2)
        self.assertEqual(dll_add_rem.head, self.dll.head)
        # Removing and adding the first item returns different prev
        dll_add_rem.remove(0)
        dll_add_rem.add(0)
        self.assertEqual(dll_add_rem.next, self.dll.next)
        self.assertEqual(dll_add_rem.prev, [1, 2, 3, 0])

if __name__ == '__main__':
    unittest.main()
