import unittest

from pages.MenuNavigationPage import MenuNavigationPage
from pages.deployments.DeploymentsPage import DeploymentsPage
from pages.deployments.DeploymentsMenuHeaderPage import DeploymentsMenuHeaderPage
from tools import ListUtils, ApiUtils
from tools.ApiUtils import ApiUtils
from tools.DriverUtils import DriverUtils
from tools.ListUtils import ListUtils
from tools.SoftAssert import SoftAssert


class IncludeComplianceActionsInDeploymentActionSectionTest(unittest.TestCase):
    """
    Test contains 2 verifications steps:
    First step validate that list of menu option that is displayed in Deployments Page is the same as an expected list
    of menu options that should be displayed.
    In the second verification steps test is validating that the deployments info grabbed from application interface are
    the same as those from API call. A list of dictionary grabbed from interface is compared with a list of dictionary
    grabbed from API call.
    """
    def setUp(self):
        self.json_list = ApiUtils().grab_json()
        self.api_deployment_info = ListUtils().grab_list_of_deployment_info(self.json_list)
        self.expected_menu_option_list=['Scan Compliance', 'Remediate', 'Change Template']

        self.browser = DriverUtils().start_driver()

    def test_IncludeComplianceActionsInDeploymentActionSectionTest(self):
        menu_navigation_page = MenuNavigationPage(self.browser)
        menu_navigation_page.navigate_to("http://localhost:8014/provision")
        menu_navigation_page.navigate_to("http://localhost:8014/provision")
        menu_navigation_page.click_on_menu_item("Deployments")
        deployment_page = DeploymentsPage(self.browser)
        aplication_deployment_info = deployment_page.create_list_of_dictionary_of_deployment_info()
        deployments_menu_header_page = DeploymentsMenuHeaderPage(self.browser)
        aplication_menu_options_list = deployments_menu_header_page.create_list_of_menu_options()

        SoftAssert().verfy_equals_true("List of menu option doesn't matched ",
                                       aplication_menu_options_list, self.expected_menu_option_list)


        SoftAssert().verfy_equals_true("List of deployments info doesn't matched ",
                                       aplication_deployment_info, self.api_deployment_info)

        self.assertEqual(SoftAssert().failures_size(), 0, str(SoftAssert().failures_list()))

    def tearDown(self):
        menuNavigationPage = MenuNavigationPage(self.browser)
        menuNavigationPage.close_driver()
