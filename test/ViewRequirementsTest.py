import unittest

from pages.MenuNavigationPage import MenuNavigationPage
from pages.LoginPage import LoginPage
from pages.LandingPage import LandingPage
from pages.policies.PoliciesPage import PoliciesPage
from pages.policies.PoliciesDetailsPage import PoliciesDetailsPage
from pages.policies.EditRequirementPage import EditRequirementPage
from tools.DriverUtils import DriverUtils
from tools.SoftAssert import SoftAssert
from tools.ConfigUtils import ConfigUtils
from tools.dataSetup.PoliciesDataSetup import PoliciesDataSetup
from tools.ListUtils import ListUtils


class ViewRequirementsTest(unittest.TestCase):
    """
    Test contain 4 verification steps:
    - is verifying that the name and description dictionary list grabbed from UI matches with the one grabbed from API
    - is verifying that the sub requirements dictionary list grabbed from UI matches with the one grabbed from API
    - is verifying that the requirement rule dictionary list grabbed from UI matches with the one grabbed from API
    - is verifying that the sub requirement rules dictionary list grabbed from UI matches with the one grabbed from API

    In te setUp phase is grabbed:
    - a random policy id
    - a random requirement id
    - a dictionary list containing requirement name and description
    - a dictionary list of sub requirements of the random requirement chosen
    - a dictionary list of rules of the random requirement chosen
    - a random sub requirements of the random requirement chosen
    - a dictionary list of sub requirement rules list

    Test:
    - is navigating to Policies page
    - is selecting a random policy by id
    - is selecting a random requirement by id
    - is grabbing requirement name and description dictionary list
    - is verifying that the name and description dictionary list grabbed from UI matches with the one grabbed from API
    - is grabbing the sub requirements dictionary list
    - is verifying that the sub requirements dictionary list grabbed from UI matches with the one grabbed from API
    - is grabbing the requirement rule dictionary list
    - is verifying that the requirement rule dictionary list grabbed from UI matches with the one grabbed from API
    - is selecting a sub requirement by id
    - is grabbing the sub requirement rules dictionary list
    - is verifying that the sub requirement rules dictionary list grabbed from UI matches with the one grabbed from API
    """

    def setUp(self):
        self.base_url = ConfigUtils().read_config_file()['baseURL']
        self.user_name = ConfigUtils().read_config_file()['userName']
        self.user_pass = ConfigUtils().read_config_file()['userPass']
        self.api_url = ConfigUtils().read_config_file()['apiBaseURL']

        self.random_policy_id = PoliciesDataSetup().grab_random_policy_id()
        self.random_requirement_id = PoliciesDataSetup().grab_random_requirement_id_by_policy_id(self.random_policy_id)
        self.requirement_name_description_dictionary_list = PoliciesDataSetup().grab_requirement_name_and_description(
            self.random_policy_id, self.random_requirement_id)
        self.sub_requirements_list = PoliciesDataSetup().grab_sub_requirements_list_by_requirement_id(
            self.random_requirement_id, self.random_policy_id)
        self.requirement_rules_list = PoliciesDataSetup().grab_requirement_rules_list_by_requirement_id(
            self.random_requirement_id, self.random_policy_id)
        self.random_sub_requirements_id = (ListUtils().return_random_from_list(self.sub_requirements_list)).get('id')
        self.sub_requirements_rules = PoliciesDataSetup().grab_sub_requirement_rule_list_by_subrequirement_id(
            self.random_requirement_id, self.random_sub_requirements_id, self.random_policy_id)

        self.browser = DriverUtils().start_driver()

    def test_ViewTemplatesTest(self):
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
        policies_details_page.select_requirement_by_id(self.random_requirement_id)

        edit_requirement_page = EditRequirementPage(self.browser)
        requirement_name_description = edit_requirement_page.grab_requirements_name_description_dictionary_list()

        SoftAssert().verfy_equals_true(
            "Requirement name and description dictionary list grabbed from API doesn't matched with list grabbed from UI",
            self.requirement_name_description_dictionary_list, requirement_name_description)

        ui_sub_requirements_list = edit_requirement_page.grab_sub_requirements()

        SoftAssert().verfy_equals_true(
            "Sub requirements list grabbed from API doesn't matched with list grabbed from UI",
            self.sub_requirements_list, ui_sub_requirements_list)

        requirement_rules = edit_requirement_page.grab_requirement_rules()
        SoftAssert().verfy_equals_true(
            "Requirement rules list grabbed from API doesn't matched with list grabbed from UI",
            self.requirement_rules_list, requirement_rules)

        edit_requirement_page.select_sub_requirement_by_id(self.random_sub_requirements_id)

        sub_requirement_rules = edit_requirement_page.grab_sub_requirement_rule()
        SoftAssert().verfy_equals_true(
            "Sub requirement rules list grabbed from API doesn't matched with list grabbed from UI",
            self.sub_requirements_rules, sub_requirement_rules)

        self.assertEqual(SoftAssert().failures_size(), 0, str(SoftAssert().failures_list()))

    def tearDown(self):
        menuNavigationPage = MenuNavigationPage(self.browser)
        menuNavigationPage.close_driver()
