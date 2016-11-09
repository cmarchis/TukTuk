import unittest

from pages.MenuNavigationPage import MenuNavigationPage
from pages.templates.TemplatesMenuListPage import TemplatesMenuListPage
from pages.templates.details.TemplateDetailsPage import TemplateDetailsPage
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

        template_menu = TemplatesMenuListPage(self.browser)
        aplication_templates_dictionary_list = template_menu.grab_templates_dictionary_list()

        SoftAssert().verfy_equals_true(
            "Templates dictionary lists doesn't matched ",
            self.template_dictionary_list, aplication_templates_dictionary_list)

        template_menu.click_on_template_by_id(self.random_template_id)

        template_details = TemplateDetailsPage(self.browser)
        aplication_template_resource_types_list = template_details.grab_resource_types_list()
        SoftAssert().verfy_equals_true("Resource Types lists doesn't matched ",
                                       self.template_resource_types_list, aplication_template_resource_types_list)

        aplication_template_policies_list = template_details.grab_policies_list()
        SoftAssert().verfy_equals_true("Policies lists doesn't matched ",
                                       self.template_policies_list, aplication_template_policies_list)

        aplication_template_deployments_list = template_details.grab_deployments_dictionary_list()
        SoftAssert().verfy_equals_true("Policies lists doesn't matched ",
                                       self.template_deployments_list, aplication_template_deployments_list)

        self.assertEqual(SoftAssert().failures_size(), 0, str(SoftAssert().failures_list()))

    def tearDown(self):
        menuNavigationPage = MenuNavigationPage(self.browser)
        menuNavigationPage.close_driver()
