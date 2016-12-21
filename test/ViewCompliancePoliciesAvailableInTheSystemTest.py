import unittest

from pages.MenuNavigationPage import MenuNavigationPage
from pages.policies.PoliciesPage import PoliciesPage

from pages.LoginPage import LoginPage
from pages.LandingPage import LandingPage
from tools.DriverUtils import DriverUtils
from tools.SoftAssert import SoftAssert
from tools.dataSetup.PoliciesDataSetup import PoliciesDataSetup
from tools.ConfigUtils import ConfigUtils


class ViewCompliancePoliciesAvailableInTheSystemTest(unittest.TestCase):
    """
    Test contain 1 verification step:
        - is VALIDATING that the list grabbed from API is the same as list of compliance grabbed from UI

    In the setUp phase is grabbed:
        - policies list available in the system

    Test:
        - is navigating to policies resource page
        - is grabbing the list of the displayed policies
        - is VALIDATING that the list grabbed from API is the same as list of compliance grabbed from UI
    """

    def setUp(self):
        self.base_url = ConfigUtils().read_config_file()['baseURL']
        self.user_name = ConfigUtils().read_config_file()['userName']
        self.user_pass = ConfigUtils().read_config_file()['userPass']
        self.api_url = ConfigUtils().read_config_file()['apiBaseURL']

        self.policies_dictionary_list = PoliciesDataSetup().grab_policies_dictionary_list()

        self.browser = DriverUtils().start_driver()

    def test_ViewDeploymentComplianceStatusOverviewTest(self):
        menu_navigation_page = MenuNavigationPage(self.browser)
        menu_navigation_page.navigate_to(self.base_url)
        menu_navigation_page.navigate_to(self.base_url)

        login_page = LoginPage(self.browser)
        login_page.perform_login(self.user_name, self.user_pass)

        landing_page = LandingPage(self.browser)
        landing_page.select_author_from_menu()

        menu_navigation_page.click_on_menu_item('Policies')

        policies_page = PoliciesPage(self.browser)
        ui_policies_list = policies_page.grab_policies_dictionary_list()

        SoftAssert().verfy_equals_true(
            "List of policies grabbed from API doesn't matched with the list grabbed from UI",
            self.policies_dictionary_list,
            ui_policies_list)

        self.assertEqual(SoftAssert().failures_size(), 0, str(SoftAssert().failures_list()))

    def tearDown(self):
        menuNavigationPage = MenuNavigationPage(self.browser)
        menuNavigationPage.close_driver()
