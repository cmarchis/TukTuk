import unittest
from test.AdHocScanComplianceAndRemediateDeploymentTest import AdHocScanComplianceAndRemediateDeploymentTest
from test.ViewDeploymentComplianceResultDetailsTest import ViewDeploymentComplianceResultDetailsTest

tests1 = unittest.TestLoader().loadTestsFromTestCase(AdHocScanComplianceAndRemediateDeploymentTest)
tests2 = unittest.TestLoader().loadTestsFromTestCase(ViewDeploymentComplianceResultDetailsTest)

all_tests = unittest.TestSuite([tests1, tests2])

unittest.TextTestRunner(verbosity=2).run(all_tests)
