#!/usr/bin/env python

"""
Execute unit tests.
"""

import sys, os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from mobius.test.test import execute_tests
return_code = execute_tests()
sys.exit(return_code)
