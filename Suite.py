import unittest
from test.IncludeComplianceActionsInDeploymentActionSectionTest import IncludeComplianceActionsInDeploymentActionSectionTest
from test.ViewDeploymentComplianceStatusOverviewTest import ViewDeploymentComplianceStatusOverviewTest
from test.ViewTemplatesTest import ViewTemplatesTest

tests1 = unittest.TestLoader().loadTestsFromTestCase(IncludeComplianceActionsInDeploymentActionSectionTest)
tests2 = unittest.TestLoader().loadTestsFromTestCase(ViewDeploymentComplianceStatusOverviewTest)
tests3 = unittest.TestLoader().loadTestsFromTestCase(ViewTemplatesTest)

all_tests = unittest.TestSuite([tests1, tests2, tests3])

unittest.TextTestRunner(verbosity=2).run(all_tests)