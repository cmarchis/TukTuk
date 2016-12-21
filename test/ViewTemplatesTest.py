import unittest

from pages.MenuNavigationPage import MenuNavigationPage
from pages.templates.TemplatesPage import TemplatesPage
from pages.templates.details.TemplateDetailsPage import TemplateDetailsPage
from pages.LoginPage import LoginPage
from pages.LandingPage import LandingPage
from tools.DriverUtils import DriverUtils
from tools.SoftAssert import SoftAssert
from tools.ConfigUtils import ConfigUtils
from tools.dataSetup.TemplateDataSetup import TemplateDataSetup


class ViewTemplatesTest(unittest.TestCase):
    """
    Test contain 4 verification steps:
    - is VALIDATING that the list of template grabbed from api matches with the list of templates grabbed from
        applications
    - is VALIDATING that the list of resources grabbed from api matches with the list of resources grabbed from
        application
    - is VALIDATING that the list of policies grabbed from api matches with the list of resources grabbed from
        applications
    - is VALIDATING that the list of deployments grabbed from api matches with the list of deployments grabbed from
        applications

    In te setUp phase is grabbed:
        - a random template
        - a random deployment id from random template
        - template list, template resource list, template policies list, template deployments list
    Test:
        - is navigating to template page
        - is grabbing the list of displayed template
        - is VALIDATING that the list of template grabbed from api matches with the list of templates grabbed from
        applications
        - is clicking on the random template
        - is grabbing the list of resources from template page
        - is VALIDATING that the list of resources grabbed from api matches with the list of resources grabbed from
        application
        - is grabbing the list of policies from template page
        - is VALIDATING that the list of policies grabbed from api matches with the list of resources grabbed from
        applications
        - is grabbing the list of deployments from template page
        - is VALIDATING that the list of deployments grabbed from api matches with the list of deployments grabbed from
        applications
    """

    def setUp(self):
        self.base_url = ConfigUtils().read_config_file()['baseURL']
        self.user_name = ConfigUtils().read_config_file()['userName']
        self.user_pass = ConfigUtils().read_config_file()['userPass']
        self.api_url = ConfigUtils().read_config_file()['apiBaseURL']

        self.random_template_id = TemplateDataSetup().get_random_template_id()
        self.random_deployment_id = TemplateDataSetup().grab_random_deployment_id_by_template_id(
            self.random_template_id)
        self.template_dictionary_list = TemplateDataSetup().grab_template_dictionary_list()
        self.template_resource_types_list = TemplateDataSetup().grab_resources_types_for_template_id(
            self.random_deployment_id)
        self.template_policies_list = TemplateDataSetup().grab_template_policies_for_template_id(
            self.random_deployment_id)
        self.template_deployments_list = TemplateDataSetup().grab_deployments_dictionary_list_for_template_id(
            self.random_deployment_id)

        self.browser = DriverUtils().start_driver()

    def test_ViewTemplatesTest(self):
        menu_navigation_page = MenuNavigationPage(self.browser)
        menu_navigation_page.navigate_to(self.base_url)
        menu_navigation_page.navigate_to(self.base_url)

        login_page = LoginPage(self.browser)
        login_page.perform_login(self.user_name, self.user_pass)

        landing_page = LandingPage(self.browser)
        landing_page.select_resource_management_from_menu()

        template_menu = TemplatesPage(self.browser)
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
        SoftAssert().verfy_equals_true("Deployments lists doesn't matched ",
                                       self.template_deployments_list, aplication_template_deployments_list)

        self.assertEqual(SoftAssert().failures_size(), 0, str(SoftAssert().failures_list()))

    def tearDown(self):
        menuNavigationPage = MenuNavigationPage(self.browser)
        menuNavigationPage.close_driver()
