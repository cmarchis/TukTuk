import unittest

from pages.MenuNavigationPage import MenuNavigationPage
from pages.LoginPage import LoginPage
from pages.LandingPage import LandingPage
from pages.policies.PoliciesPage import PoliciesPage
from pages.policies.PoliciesDetailsPage import PoliciesDetailsPage
from pages.policies.ClonePolicyPage import ClonePolicyPage
from tools.ConfigUtils import ConfigUtils
from tools.DriverUtils import DriverUtils
from tools.SoftAssert import SoftAssert
from tools.dataSetup.PoliciesDataSetup import PoliciesDataSetup
from tools.StringUtils import StringUtils


class EditPolicyPropertiesFromUITest(unittest.TestCase):
    """
    Test contain 1 verification steps:
    - is verifying that the list of values grabbed from UI after editing matches with the list of values gabbed from
    UI, from Policies page,  after save operation

    In te setUp phase is grabbed:
    - a random policy id

    Test:
    - is navigating to Policies page
    - is selecting a policy by it's id
    - is clicking on Clone policy button
    - is editing policy name, description, type
    - is grabbing the list of displayed values of edited fields
    - is clicking on save button
    - is grabbing the list of edited values from Policies pages list
    - is verifying that the list of values grabbed from UI after editing matches with the list of values gabbed from
    UI, from Policies page,  after save operation
    """

    def setUp(self):
        self.base_url = ConfigUtils().read_config_file()['baseURL']
        self.user_name = ConfigUtils().read_config_file()['userName']
        self.user_pass = ConfigUtils().read_config_file()['userPass']
        self.api_url = ConfigUtils().read_config_file()['apiBaseURL']

        self.random_policy_id = PoliciesDataSetup().grab_random_policy_id()

        self.policy_name = 'Name' + StringUtils().generate_random_string_number(999)
        self.policy_description = 'Description' + StringUtils().generate_random_string_number(999)

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
        policies_page.select_policy_by_policy_id(self.random_policy_id)
        policies_details_page = PoliciesDetailsPage(self.browser)
        policies_details_page.click_edit_policy_button()

        clone_policy_page = ClonePolicyPage(self.browser)
        random_policy = clone_policy_page.grab_random_policy_type()
        clone_policy_page.edit_policy(self.policy_name, self.policy_description, random_policy)
        clone_policies_dictionary_list = clone_policy_page.grab_policy_dictionary_list()
        clone_policy_page.click_save_button()

        policies_after_clone = policies_page.grab_policies_dictionary_list_for_policy_id(self.random_policy_id)

        SoftAssert().verfy_equals_true(
            "Edit policy properties doesn't work as expected",
            clone_policies_dictionary_list, policies_after_clone)

        self.assertEqual(SoftAssert().failures_size(), 0, str(SoftAssert().failures_list()))

    def tearDown(self):
        menuNavigationPage = MenuNavigationPage(self.browser)
        menuNavigationPage.close_driver()
