# ferecrystal_isomers
This is a Python module to calculate isomers of ferecrystalline compounds. The concept of ferecrystal isomers was introduced by Esters et al. (DOI: 10.1002/anie.201409714) for ferecrystals with two components. This module calculates all isomers for up to 26 different components using the algorithm for generating bracelets with fixed content by Karim et al. (DOI: 10.1016/j.tcs.2012.11.024). The isomers can be filtered by thickness of the individual components and by desired or undesired interfaces.

# Usage
The py files can be used as is and do not require any packages not present in a standard python installation. The easiest way to use this module is to change the 'print_isomers.py' file. Detailed instructions are presented in there.

# Requirements
The module uses string and copy, which are part of the standard Python installation. For the unittest, the package six is required for Python 2 and 3 compatibility.
