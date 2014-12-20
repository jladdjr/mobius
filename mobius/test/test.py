#!/usr/bin/env python

"""
Test for Mobius.
"""

import unittest
import xmlrunner

class MobiusTest(unittest.TestCase):
    """
    Tests Mobius.
    """

    def test_run(self):
        """
        Test run() method.
        """
        from mobius.main import Main

        main = Main()
        result = main.run()

        self.assertEqual(result, 0)

#Execute tests
def execute_tests():
    """
    Runs all tests.
    """
    #unittest.main(testRunner=xmlrunner.XMLTestRunner(output='test-reports'))
    suite = unittest.TestLoader().loadTestsFromTestCase(MobiusTest)
    result = xmlrunner.XMLTestRunner(output='test-reports').run(suite)
    failures_and_errors = len(result.failures) + len(result.errors)
    return failures_and_errors 
