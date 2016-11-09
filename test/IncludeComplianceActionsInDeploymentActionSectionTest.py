import unittest

from pages.MenuNavigationPage import MenuNavigationPage
from pages.deployments.DeploymentsMenuHeaderPage import DeploymentsMenuHeaderPage
from pages.deployments.DeploymentsPage import DeploymentsPage
from pages.templates.TemplatesMenuListPage import TemplatesMenuListPage
from pages.templates.details.TemplateDetailsPage import TemplateDetailsPage
from pages.LoginPage import LoginPage
from pages.LandingPage import LandingPage
from tools.DriverUtils import DriverUtils
from tools.SoftAssert import SoftAssert
from tools.ConfigUtils import ConfigUtils
from tools.api.mock.DataSetup import DataSetup



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
        self.base_url = ConfigUtils().read_config_file()['baseURL']
        self.user_name = ConfigUtils().read_config_file()['userName']
        self.user_pass = ConfigUtils().read_config_file()['userPass']
        self.api_url = ConfigUtils().read_config_file()['apiBaseURL']

        self.expected_menu_option_list = ['Scan Compliance', 'Remediate', 'Change Template']

        self.random_template_id = DataSetup().get_random_template_id()
        self.random_deployment_id = DataSetup().grab_random_deployment_by_template_id(self.random_template_id)
        self.api_deployment_info = DataSetup().grab_deployment_info_from_templates(self.random_deployment_id)
        self.browser = DriverUtils().start_driver()

    def test_IncludeComplianceActionsInDeploymentActionSectionTest(self):
        menu_navigation_page = MenuNavigationPage(self.browser)
        menu_navigation_page.navigate_to(self.base_url)
        menu_navigation_page.navigate_to(self.base_url)

        login_page = LoginPage(self.browser)
        login_page.perform_login(self.user_name, self.user_pass)

        landing_page = LandingPage(self.browser)
        landing_page.select_provision()

        templates_menu_list_page = TemplatesMenuListPage(self.browser)
        templates_menu_list_page.click_on_template_by_id(self.random_template_id)

        template_details_page = TemplateDetailsPage(self.browser)
        template_details_page.select_deployment_by_id(self.random_deployment_id)

        deployment_page = DeploymentsPage(self.browser)

        aplication_deployment_info = deployment_page.create_list_of_dictionary_of_deployment_info()
        deployments_menu_header_page = DeploymentsMenuHeaderPage(self.browser)
        aplication_menu_options_list = deployments_menu_header_page.create_list_of_menu_options()

        SoftAssert().verfy_equals_true("List of menu option doesn't matched ", self.expected_menu_option_list,
                                       aplication_menu_options_list)

        SoftAssert().verfy_equals_true("List of deployments info doesn't matched ", self.api_deployment_info,
                                       aplication_deployment_info)

        self.assertEqual(SoftAssert().failures_size(), 0, str(SoftAssert().failures_list()))

    def tearDown(self):
        menuNavigationPage = MenuNavigationPage(self.browser)
        menuNavigationPage.close_driver()
