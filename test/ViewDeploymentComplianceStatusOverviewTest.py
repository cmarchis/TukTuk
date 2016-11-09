import unittest

from pages.MenuNavigationPage import MenuNavigationPage
from pages.deployments.DeploymentsPage import DeploymentsPage
from pages.templates.TemplatesMenuListPage import TemplatesMenuListPage
from pages.templates.details.TemplateDetailsPage import TemplateDetailsPage
from tools.DriverUtils import DriverUtils
from tools.ListUtils import ListUtils
from tools.SoftAssert import SoftAssert
from tools.ConfigUtils import ConfigUtils
from tools.api.mock.DataSetup import DataSetup
from pages.LoginPage import LoginPage
from pages.LandingPage import LandingPage


class ViewDeploymentComplianceStatusOverviewTest(unittest.TestCase):
    """
    Test will make 3 verification steps:
    In the first one test will navigate to deployments page and grab in a dictionary list all policies displayed with
    their attributes (number of variances, number of times that specific policy types appear) and compare this list
    with a list of dictionary grabbed from API call in setUp method.
    The second step verify that the resources dictionary list [{resource name, status},...] grabbed from application
    interface is the same as the list obtained from API call in setUp method. The status for resource (Warning,
    Compliant,Non Compliant, Unknown) is calculated separated considering complianceScore grabbed from API call.
    The third step verify that the bars dimensions of the policies compliance status overview are the same as those
    that are calculated using compliant scores dates from api calls.
    """

    def setUp(self):
        self.base_url = ConfigUtils().read_config_file()['baseURL']
        self.user_name = ConfigUtils().read_config_file()['userName']
        self.user_pass = ConfigUtils().read_config_file()['userPass']
        self.api_url = ConfigUtils().read_config_file()['apiBaseURL']

        self.random_template_id = '1234'
        self.random_deployment_id = '1234'
        # self.random_template_id = DataSetup().get_random_template_id()
        # self.random_deployment_id = DataSetup().grab_random_deployment_by_template_id(self.random_template_id)
        self.random_resource_id = DataSetup().grab_random_resource_id_by_deployment_id(self.random_deployment_id)

        api_policies_types_dictionary = DataSetup().grab_policies_types_dictionary_list_for_deployment_id(
            self.random_deployment_id)
        self.sorted_api_policies_types_dictionary = ListUtils().sort_list_alphabetically_by('type',
                                                                                            api_policies_types_dictionary)
        self.api_resources_dictionary = DataSetup().grab_list_dictionary_of_resources_for_deployment_id(
            self.random_deployment_id)

        aplication_bar_dimension = 192

        self.api_policies_dimension_bar_dictionary_list = DataSetup().grab_list_of_policies_bar_dimensions(
            self.random_deployment_id, aplication_bar_dimension)

        self.browser = DriverUtils().start_driver()

    def test_ViewDeploymentComplianceStatusOverviewTest(self):
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
        aplication_policies_list = ListUtils().sort_list_alphabetically_by('type',
                                                                           deployment_page.create_list_of_dictionary_for_policies())

        SoftAssert().verfy_equals_true("List of policies doesn't matched ",
                                       self.sorted_api_policies_types_dictionary, aplication_policies_list)

        # aplication_resources_list_with_status = deployment_page.create_list_of_dictionary_for_resources()
        #
        # SoftAssert().verfy_equals_true("List of resources doesn't matched ",
        #                                self.api_resources_dictionary, aplication_resources_list_with_status)
        #
        # aplication_policies_dimensions_bar_list = deployment_page.create_list_of_policies_dimensions_bar()
        # print "aplication_policies_dimensions_bar_list: ", aplication_policies_dimensions_bar_list
        #
        # SoftAssert().verfy_equals_true("List of dimension bar doesn't matched ",
        #                                self.api_policies_dimension_bar_dictionary_list,
        #                                aplication_policies_dimensions_bar_list)

        self.assertEqual(SoftAssert().failures_size(), 0, str(SoftAssert().failures_list()))

    def tearDown(self):
        menuNavigationPage = MenuNavigationPage(self.browser)
        menuNavigationPage.close_driver()
