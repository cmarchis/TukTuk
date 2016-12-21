import unittest
from test.ViewRequirementsTreeTest import ViewRequirementsTreeTest
from test.ViewPolicyDetailsTest import ViewPolicyDetailsTest

tests1 = unittest.TestLoader().loadTestsFromTestCase(ViewRequirementsTreeTest)
tests2 = unittest.TestLoader().loadTestsFromTestCase(ViewPolicyDetailsTest)

all_tests = unittest.TestSuite([tests1, tests2])

unittest.TextTestRunner(verbosity=2).run(all_tests)
