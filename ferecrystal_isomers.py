"""
This module creates all ferecrystal isomers with a given composition.
It also has a method to filter isomers according to thickness or
interface criteria (see function get_isomer subset for details). It
uses the algorithm by Karim et al. to create bracelets with fixed
content to create the isomers (see bracelets module for full citation).
"""

__author__ = "Marco Esters"
__copyright__ = "Copyright 2017, Marco Esters"
__version__ = "1.0"
__maintainer__ = "Marco Esters"
__email__ = "esters@uoregon.edu"
__date__ = "03/06/2017"

from bracelets import Bracelets
from string import ascii_uppercase


class Isomers(object):
    """
    Isomer class to generate all ferecrystal isomers. Uses the
    algorithm Karim et al. (DOI: 10.1016/j.tcs.2012.11.024) to
    generate bracelets with fixed content.
    """
    def __init__(self, composition, elements=None):
        """
        Checks for invalid input and generates all isomers.

        Args:
            composition (list or tuple): A list or tuple representation
                of the formula of the ferecrystal repeating unit.
                List items must be integers.
            elements (list or tuple): A list or a touple of the
                constituents in the ferecrystal for the output of the
                isomers. The list must have the same length as the
                composition, and the list items must be string.
                Defaults to None. If it is None, uppercase letters are
                used for the output instead.
        """
        if not (isinstance(composition, list)
                or isinstance(composition, tuple)):
            raise TypeError('Composition must be list or tuple')
        if len(composition) < 2:
            raise ValueError('Composition must have at least 2 items.')
        if len(composition) > 26:
            raise ValueError('Composition cannot have more than 26 items.')
        for i in composition:
            if not isinstance(i, int):
                raise TypeError('Values must be a integers.')
        self._composition = composition
        if elements is not None:
            if not (isinstance(elements, list)
                    or isinstance(elements, tuple)):
                raise TypeError('Elements must be None, list, or tuple.')
            if len(self._composition) != len(elements):
                raise ValueError('Elements must be of the '
                                 'same size as composition.')
            for element in elements[:-1]:
                if elements.count(element) > 1:
                    raise ValueError('Element list contains duplicates.')

        self._elements = elements
        self._bracelets = Bracelets(composition)
        self._all_isomers = self._isomers_from_bracelets()

    def _as_tuples(self):
        """
        Converts the bracelets into isomer tuples, i.e. the numbers
        be replaced with the element strings.
        """
        isomer_tuples = []
        for brac in self._bracelets.as_tuple():
            isomer = [(self._elements[t[0]], t[1]) for t in brac]
            isomer_tuples.append(isomer)
        return isomer_tuples

    def _isomers_from_bracelets(self):
        """
        Formats the tuples returned from the bracelet algorithm and
        outputs a list of formatted strings
        """
        isomers = []
        for brace in self._bracelets.as_tuple():
            istring = ''
            for b in range(len(brace)):
                if self._elements is None:
                    letter = ascii_uppercase[brace[b][0]]
                else:
                    letter = self._elements[brace[b][0]]
                istring = '%s(%s)%d' % (istring, letter, brace[b][1])
                if b != len(brace) - 1:
                    istring = '%s-' % istring
            isomers.append(istring)
        return isomers

    def _isomers_from_tuples(self, isomers):
        """
        Converts the isomer tuples into string. This function converts
        the output of 'get_isomer_subset' into a list of strings.
        Args:
            isomers (list): A list of isomers as tuples.

        """
        isomer_tuples = []
        for isomer in isomers:
            istring = ''
            for t in range(len(isomer)):
                istring += '(%s)%d' % (isomer[t][0], isomer[t][1])
                if t != len(isomer) - 1:
                    istring += '-'
            isomer_tuples.append(istring)

        return isomer_tuples

    def _transform_to_letter(self, element_string):
        """
        Transforms the isomers strings that use elements instead of
        uppercase letters into a string of uppercase letters to
        simplify the interface filter. The function sorts the elements
        by length in reverse order so that e.g. 'SnSe2' is not seen as
        'SnSe' by the algorithm.

        Args:
            element_string (string): An isomer as a concatenated string
                of its constituents.
        """
        element_indices = {self._elements[i]: i
                           for i in range(len(self._elements))}
        for element in sorted(self._elements[:])[::-1]:
            letter = ascii_uppercase[element_indices[element]]
            element_string = element_string.replace(element, letter)
        return element_string

    def _filter_interface(self, isomers, interface_conditions):
        """
        A function to return only the isomers that satisfy the
        thickness conditions.

        Args:
            isomers (list): A list of tuples with either all isomers or
                            the isomers that remain after going through
                            the thickness filter.
            interface_conditions (dict): The interface conditions as
                described in the function 'get_isomer_subset'.
        """
        filtered_isomers = []
        inter_cond = interface_conditions.copy()
        if self._elements is not None:
            for key in inter_cond:
                newkey = self._transform_to_letter(key)
                inter_cond[newkey] = inter_cond.pop(key)
        for isomer in isomers:
            append_isomer = True
            istring = ''.join([i[0]*i[1] for i in isomer])
            if self._elements is not None:
                istring = self._transform_to_letter(istring)
            for key in inter_cond:
                val = inter_cond[key]
                if type(val) is bool:
                    interface = key in istring or key[::-1] in istring
                    if interface != inter_cond[key]:
                        append_isomer = False
                        break
                else:
                    istring_extd = istring + istring[0:len(key)-1]
                    occ = istring.count(key)
                    if key != key[::-1]:
                        occ += istring.count(key[::-1])

                    if occ < val[0] or (val[1] > 0 and occ > val[1]):
                        append_isomer = False
                        break
            if append_isomer:
                filtered_isomers.append(isomer)
        return filtered_isomers

    def _filter_thickness(self, isomers, thickness_conditions):
        """
        A function to return only the isomers that satisfy the
        thickness conditions.

        Args:
            isomers (list): All isomers as a list of tuples.
            thickness_conditions (dict): The thickness conditions as
                described in the function 'get_isomer_subset'.
        """
        filtered_isomers = []
        intvals = {key: False for key in thickness_conditons
                   if type(thickness_conditions[key]) is int}
        for isomer in isomers:
            append_isomer = True
            intvals = {key: False for key in intvals}
            for i in isomer:
                if i[0] in thickness_conditions:
                    val = thickness_conditions[i[0]]
                    if type(val) is int and i[1] == val:
                        intvals[i[0]] = True
                    elif i[1] < val[0] or (val[1] > 0 and i[1] > val[1]):
                        append_isomer = False
                        break
            if append_isomer and False not in intvals.values():
                filtered_isomers.append(isomer)
        return filtered_isomers

    def get_formula(self):
        """
        Returns the chemical formula of the ferecrystal as a string.
        """
        formula_string = ''
        for i in range(len(self._composition)):
            formula_string += '(%s)%d' % (self._elements[i],
                                          self._composition[i])
        return formula_string

    def get_isomer_subset(self,
                          thickness_conditions=None,
                          interface_conditions=None):
        """
        Overhead function to filter isomers based on the input
        thickness and interface conditions.
        Args:
            interface_donditions (dict):
                A dictionary describing interface conditions. Defaults
                to None. Dictionary keys are entered as they would
                appear in the isomer. Examples:
                    * 'PbSeSnSe' checks for interfaces between one PbSe
                      and one SnSe layer. Note that the occurrence of
                      PbSe-SnSe-PbSe constitutes two interfaces.
                    * To check for occurrences of '(PbSe)2(SnSe)2', the
                      key 'PbSePbSeSnSeSnSe' needs to be used.

                Acceptable value formats:
                    False: Returns only isomers where the interface(s)
                           described in the key do(es) not exist. For
                           example {'PbSeSnSe': False} omits all
                           isomers with a PbSe-SnSe interface.

                    True: Returns any isomers that have the interface(s)
                          described in the key. Equivalent to (1, 0).

                    int: Returns isomers that have exactly 'int' number
                         of interface(s) described in the key.

                    (int1, int2): Returns isomers with at least 'int1'
                                  and at most 'int2' number of
                                  occurrences of the interface(s)
                                  described in the key.

                    (0, int2): Returns isomers with at most 'int2'
                               number of occurences of the interface(s)
                               described in the key.

                (int1, 0): Returns isomers with at least 'int1' number
                           of occurences of the interface(s) described
                           in the key. (1, 0) is equivalend to True.

        thickness_conditions (dict):
            A dictionary describing thickness conditions for each
            element. Defaults to None. Acceptable value formats:

                int: Returns isomers with at least one instance of the
                     element with thickness 'int' (integer). To return
                     isomers where the element exclusively has the
                     thickness 'int', use (int, int).


                (int1, int2): Returns isomers with a thickness of the
                              element of at least 'int1' and at most
                              'int2'. Can also be of format list.

                (0, int2): Returns isomers with a maximum thickness of
                           the element of 'int2'. Can also be a list.

                (int1, 0): Returns isomers with a minimum thickness of
                           the element of 'int1'. Can also be a list.
        """
        isomer_subset = self._as_tuples()
        if thickness_conditions is not None:
            if not isinstance(thickness_conditions, dict):
                raise ValueError('Thickness conditions must be a dictionary.')
            else:
                for key in thickness_conditions:
                    val = thickness_conditions[key]
                    if type(val) is int:
                        thickness_conditions[key] = [val, val]
                isomer_subset = self._filter_thickness(isomer_subset,
                                                       thickness_conditions)
        if interface_conditions is not None:
            if not isinstance(interface_conditions, dict):
                raise ValueError('Interface conditions must be a dictionary.')
            for key in interface_conditions:
                val = interface_conditions[key]
                if type(val) is int:
                    interface_conditions[key] = [val, val]
            isomer_subset = self._filter_interface(isomer_subset,
                                                   interface_conditions)
        return self._isomers_from_tuples(isomer_subset)

    @property
    def isomers(self):
        """
        Returns all isomers as a list of formatted strings.
        """
        return self._all_isomers
