import unittest

from pages.MenuNavigationPage import MenuNavigationPage
from pages.templates.TemplatesMenuListPage import TemplatesMenuListPage
from pages.policies.PoliciesListPage import PoliciesListPage
from pages.LoginPage import LoginPage
from pages.LandingPage import LandingPage
from tools.DriverUtils import DriverUtils
from tools.SoftAssert import SoftAssert
from tools.ConfigUtils import ConfigUtils
from tools.api.mock.DataSetup import DataSetup


class ViewTemplatesTest(unittest.TestCase):

    def setUp(self):
        self.base_url = ConfigUtils().read_config_file()['baseURL']
        self.user_name = ConfigUtils().read_config_file()['userName']
        self.user_pass = ConfigUtils().read_config_file()['userPass']
        self.api_url = ConfigUtils().read_config_file()['apiBaseURL']

        self.random_template_id = DataSetup().get_random_template_id()
        self.random_deployment_id = DataSetup().grab_random_deployment_by_template_id(self.random_template_id)
        self.template_dictionary_list = DataSetup().grab_template_dictionary_list()
        self.template_resource_types_list = DataSetup().grab_template_resources_types_for_template_id(
            self.random_deployment_id)
        self.template_policies_list = DataSetup().grab_template_policies_for_template_id(
            self.random_deployment_id)
        self.template_deployments_list = DataSetup().grab_template_deployments_for_template_id(
            self.random_deployment_id)

        self.browser = DriverUtils().start_driver()

    def test_ViewTemplatesTest(self):
        menu_navigation_page = MenuNavigationPage(self.browser)
        menu_navigation_page.navigate_to(self.base_url)
        menu_navigation_page.navigate_to(self.base_url)

        login_page = LoginPage(self.browser)
        login_page.perform_login(self.user_name, self.user_pass)

        landing_page = LandingPage(self.browser)
        landing_page.select_provision()
        menu_navigation_page.click_on_menu_item("Policies")

        policies_page = PoliciesListPage(self.browser)
        policies_data = policies_page.grab_policies_dictionary_list()
        print policies_data