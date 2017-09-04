"""
This script prints isomers of ferecrystals and filters isomers that
do not conform with the thickness and interface limitations specified
by the user.

To use this script, simply change the following variables:

composition: A list of integers that represents the composition of the
             ferecrystal. Example: the list [2, 3, 4] generates all
             isomers with the composition (A)2(B)3(C)4.
             The maximum number of items is 26.

elements: A list of string that is purely decorative. Each component
          in the isomer will be printed using the strings in the list.
          If this is not desired, elements can be set to None or
          deleted entirely. If it is deleted, it must also be removed
          from when Isomers is called).
          Must have the same number of items as composition or be None.

iface: A dictionary describing interface conditions. Dictionary keys
       are entered as they would appear in the isomer. Examples:
           * 'PbSeSnSe' checks for interfaces between one PbSe and one
              SnSe layer. Note that the occurrence of PbSe-SnSe-PbSe
              constitutes two interfaces.
           * To check for occurrences of '(PbSe)2(SnSe)2', the key
             'PbSePbSeSnSeSnSe' needs to be used.

       Acceptable value formats:

           False: Returns only isomers where the interface(s) described
                  in the key does not exist. E.g. {'PbSeSnSe': False}
                  omits all isomers with a PbSe-SnSe interface.

           True: Returns any isomer that has the interface(s)
                 described in the key. Equivalent to (1, 0)

           int: Returns isomers that have exactly 'int' number of
                interface(s) described in the key

           (int1, int2): Returns isomers with at least 'int1' and at
                         most 'int2' number of occurrences of the
                         interface(s) described in the key

           (0, int2): Returns isomers with at most 'int2' number of
                      occurences of the interface(s) described in the
                      key.

           (int1, 0): Returns isomers with at least 'int1' number of
                      occurences of the interface(s) described in the
                      key. The value (1, 0) is equivalend to True.

thickness: A dictionary describing thickness conditions for each
           element. Acceptable value formats:

               int: Returns isomers with at least one instance of the
                    element with thickness 'int' (integer). To return
                    isomers where the element exclusively has the
                    thickness 'int', use (int, int).


               (int1, int2): Returns isomers with a thickness of the
                             element of at least 'int1' and at most
                             'int2'. Can also be a list.

               (0, int2): Returns isomers with a maximum thickness of
                          the element of 'int2'. Can also be a list.

               (int1, 0): Returns isomers with a minimum thickness of
                          the element of 'int1'. Can also be a list.

"""

from __future__ import division, unicode_literals, print_function
from ferecrystal_isomers import Isomers

if __name__ == '__main__':
    composition = [2, 2, 2]
    elements = ['TiSe2', 'VSe2', 'PbSe']
    iface = None    # Example dictionary entry: {'TiSe2VSe2': False}
    thickness = None    # Example dictionary entry: {'PbSe': 2}
    isomers = Isomers(composition, elements)
    formula = isomers.get_formula()

    if iface is None and thickness is None:
        print "Number of isomers for %s: %d" % (formula, len(isomers.isomers))
        print "Printing all isomers:"
        for isomer in isomers.isomers:
            print isomer
    else:
        subset = isomers.get_isomer_subset(interface_conditions=iface,
                                           thickness_conditions=thickness)
        print "Number of isomers for %s"\
              " with selected conditions: %d" % (formula, len(subset))
        print "Printing subset:"
        for isomer in subset:
            print isomer
