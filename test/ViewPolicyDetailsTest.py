import unittest

from pages.MenuNavigationPage import MenuNavigationPage
from pages.LoginPage import LoginPage
from pages.LandingPage import LandingPage
from pages.policies.PoliciesPage import PoliciesPage
from pages.policies.PoliciesDetailsPage import PoliciesDetailsPage
from tools.ConfigUtils import ConfigUtils
from tools.DriverUtils import DriverUtils
from tools.SoftAssert import SoftAssert
from tools.dataSetup.PoliciesDataSetup import PoliciesDataSetup


class ViewPolicyDetailsTest(unittest.TestCase):
    """
    Test contains 1 verification steps:
        - is VALIDATING that the list of requirements grabbed from API matches with te list of requirements grabbed
        from UI

    In the setUp phase is grabbed:
        - a random policy id
        - requirements dictionary list grabbed for random policy id

    Test:
        - is navigating to Policies page
        - is selecting a random policy by id
        - is grabbing the list of requirements displayed
        - is VALIDATING that the list of requirements grabbed from API mathces with te list of requirements grabbed
        from UI
    """

    def setUp(self):
        self.base_url = ConfigUtils().read_config_file()['baseURL']
        self.user_name = ConfigUtils().read_config_file()['userName']
        self.user_pass = ConfigUtils().read_config_file()['userPass']
        self.api_url = ConfigUtils().read_config_file()['apiBaseURL']

        self.random_policy_id = PoliciesDataSetup().grab_random_policy_id()

        self.api_requirements_name_id_list = PoliciesDataSetup().grab_requirements_name_list_by_policy_id(
            self.random_policy_id)

        self.browser = DriverUtils().start_driver()

    def test_ViewPolicyDetailsTest(self):
        menu_navigation_page = MenuNavigationPage(self.browser)
        menu_navigation_page.navigate_to(self.base_url)
        menu_navigation_page.navigate_to(self.base_url)

        login_page = LoginPage(self.browser)
        login_page.perform_login(self.user_name, self.user_pass)

        landing_page = LandingPage(self.browser)
        landing_page.select_author_from_menu()

        menu_navigation_page.click_on_menu_item('Policies')

        policies_page = PoliciesPage(self.browser)
        policies_page.select_policy_by_policy_id(self.random_policy_id)
        policies_details_page = PoliciesDetailsPage(self.browser)
        ui_requirements_name_id_list = policies_details_page.grab_requirements_name_and_id_list()

        SoftAssert().verfy_equals_true(
            "List of requirements grabbed from API doesn't matched with the list grabbed from UI",
            self.api_requirements_name_id_list,
            ui_requirements_name_id_list)

        self.assertEqual(SoftAssert().failures_size(), 0, str(SoftAssert().failures_list()))

    def tearDown(self):
        menuNavigationPage = MenuNavigationPage(self.browser)
        menuNavigationPage.close_driver()
