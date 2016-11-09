import unittest
from operator import itemgetter

from pages.MenuNavigationPage import MenuNavigationPage
from pages.compliance.CompliancePage import CompliancePage
from pages.deployments.DeploymentsPage import DeploymentsPage
from pages.templates.TemplatesMenuListPage import TemplatesMenuListPage
from pages.templates.details.TemplateDetailsPage import TemplateDetailsPage
from pages.LoginPage import LoginPage
from pages.LandingPage import LandingPage
from tools.DriverUtils import DriverUtils
from tools.ListUtils import ListUtils
from tools.SoftAssert import SoftAssert
from tools.api.mock.DataSetup import DataSetup
from tools.ConfigUtils import ConfigUtils


class ViewDeploymentComplianceResultDetailsTest(unittest.TestCase):
    def setUp(self):
        self.base_url = ConfigUtils().read_config_file()['baseURL']
        self.user_name = ConfigUtils().read_config_file()['userName']
        self.user_pass = ConfigUtils().read_config_file()['userPass']
        self.api_url = ConfigUtils().read_config_file()['apiBaseURL']

        self.random_template_id = DataSetup().get_random_template_id()
        self.random_deployment_id = DataSetup().grab_random_deployment_by_template_id(self.random_template_id)
        self.random_resource_id = DataSetup().grab_random_resource_id_by_deployment_id(self.random_deployment_id)

        self.number_of_compliance = DataSetup().get_number_of_compliance(self.random_resource_id)
        compliance_list_by_resource = DataSetup().grab_compliance_list_by_resource(self.random_resource_id)
        self.api_sorted_compliance_dictionary = sorted(compliance_list_by_resource,
                                                       key=itemgetter('name', 'key', 'status'))
        self.status = 'Compliant'
        api_compliance_list_by_resource_of_given_status = DataSetup().grab_compliance_list_by_resource_of_given_status(
            self.random_resource_id, self.status)
        self.sorted_api_compliance_list_by_resource_of_given_status = sorted(
            api_compliance_list_by_resource_of_given_status,
            key=itemgetter('name', 'key', 'status'))
        self.sort_option = 'Requirement'
        api_compliance_list_by_resources_sorted_by_given_option = DataSetup().grab_compliance_list_by_resources_sorted_by_key(
            self.sort_option, self.random_resource_id)
        self.sorted_api_compliance_list_by_resources_sorted_by_given_option = ListUtils().sort_list_dictionary_natural_ascending(
            api_compliance_list_by_resources_sorted_by_given_option)
        self.sorted_api_compliance_list_by_resources_sorted_ordered_by_given_option = ListUtils().sort_list_dictionary_natural_descending(
            api_compliance_list_by_resources_sorted_by_given_option)

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
        deployment_page.select_resource_by_id(self.random_resource_id)

        compliance_page = CompliancePage(self.browser)
        compliance_page.scroll_until_all_compliance_are_visible(self.number_of_compliance)
        aplication_compliance_list = compliance_page.create_list_of_dictionary_for_compliance()

        aplication_sorted_compliance_dictionary = sorted(aplication_compliance_list,
                                                         key=itemgetter('name', 'key', 'status'))

        SoftAssert().verfy_equals_true(
            "List of compliance grabbed from API doesn't matches with the one grabbed from UI ",
            self.api_sorted_compliance_dictionary,
            aplication_sorted_compliance_dictionary)

        compliance_page.select_status(self.status)

        compliance_page.scroll_until_all_compliance_are_visible(self.number_of_compliance)
        aplication_compliance_filter_list_dictionary = compliance_page.create_list_of_dictionary_for_compliance()
        aplication_compliance_filter_list_dictionary_sorted = sorted(aplication_compliance_filter_list_dictionary,
                                                                     key=itemgetter('name', 'key', 'status'))

        SoftAssert().verfy_equals_true(
            "List of compliance, filter by status, grabbed from API and doesn't matches with the one grabbed from UI ",
            self.sorted_api_compliance_list_by_resource_of_given_status,
            aplication_compliance_filter_list_dictionary_sorted)

        compliance_page.select_status('All')
        compliance_page.select_sort_option(self.sort_option)
        #
        compliance_page.scroll_until_all_compliance_are_visible(self.number_of_compliance)
        aplication_compliance_list_dictionary_sort = compliance_page.create_list_of_dictionary_for_compliance()

        SoftAssert().verfy_equals_true(
            "List of compliance, sorted, grabbed from API and doesn't matches with the one grabbed from UI ",
            self.sorted_api_compliance_list_by_resources_sorted_by_given_option,
            aplication_compliance_list_dictionary_sort)

        compliance_page.select_sort_order('descending')
        compliance_page.scroll_until_all_compliance_are_visible(self.number_of_compliance)
        aplication_compliance_list_dictionary_sort_order = compliance_page.create_list_of_dictionary_for_compliance()

        SoftAssert().verfy_equals_true(
            "List of compliance, sorted,ordered, grabbed from API and doesn't matches with the one grabbed from UI ",
            self.sorted_api_compliance_list_by_resources_sorted_ordered_by_given_option,
            aplication_compliance_list_dictionary_sort_order)

        self.assertEqual(SoftAssert().failures_size(), 0, str(SoftAssert().failures_list()))

    def tearDown(self):
        menuNavigationPage = MenuNavigationPage(self.browser)
        menuNavigationPage.close_driver()
