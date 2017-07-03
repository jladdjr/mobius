#!/usr/bin/env python

# Ignore lowercase constant names (in bottom section)
# pylint: disable=C0103

"""
Test for Mobius.
"""
from mobius.mobius import main
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
        mob = main.Main()
        result = mob.run()

        self.assertEqual(result, 0)

if __name__ == '__main__':
    # unittest.main(testRunner=xmlrunner.XMLTestRunner(output='test-reports'))
    suite = unittest.TestLoader().loadTestsFromTestCase(MobiusTest)
    testResult = xmlrunner.XMLTestRunner(output='test-reports').run(suite)
    failures_and_errors = len(testResult.failures) + len(testResult.errors)
    exit(failures_and_errors)
