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


class ViewComplianceTest(unittest.TestCase):
    """
    Test contain 4 verification steps:
        - is VALIDATING that the list grabbed from api is the same as list of compliance grabbed from application
        - is VALIDATING that the list grabbed from api is the same as list of compliance grabbed from application
            after  status filter is applied
        - is VALIDATING that the list grabbed from api is the same as list of compliance grabbed from application
            sort option is applied
        - is VALIDATING that the list grabbed from api is the same as list of compliance grabbed from application
            after  sort option descending is applied

    In te setUp phase is grabbed:
                                    - compliance list for all resources
                                    - compliance list displayed by a given status
                                    - compliance list sorted by given sort option
    Test: - is navigating to compliance resource page.
            - is scrolling till all the compliance are visible
            - is grabbing the list of the displayed compliance
            - is VALIDATING that the list grabbed from api is the same as list of compliance grabbed from application
            - is selecting a status for compliance
            - is scrolling till all the compliance are visible
            - is grabbing the compliance list after  status filter is applied
            - is VALIDATING that the list grabbed from api is the same as list of compliance grabbed from application
            after  status filter is applied
            - is disable-ing status filter
            - is selecting a sorting option
            - is scrolling till all the compliance are visible
            - is grabbing the compliance list after  sort option is applied
            - is VALIDATING that the list grabbed from api is the same as list of compliance grabbed from application
            sort option is applied
            - is selecting descending order from sorting option
            - is scrolling till all the compliance are visible
            - is grabbing the compliance list after  sort option descending is applied
            - is VALIDATING that the list grabbed from api is the same as list of compliance grabbed from application
            after  sort option descending is applied
    """

    def setUp(self):
        self.base_url = ConfigUtils().read_config_file()['baseURL']
        self.user_name = ConfigUtils().read_config_file()['userName']
        self.user_pass = ConfigUtils().read_config_file()['userPass']
        self.api_url = ConfigUtils().read_config_file()['apiBaseURL']

        compliance_list_by_resource = DataSetup().grab_all_compliance_list()
        self.api_sorted_compliance_dictionary = sorted(compliance_list_by_resource,
                                                       key=itemgetter('name', 'key', 'status'))
        self.status = 'Compliant'
        api_compliance_list_by_resource_of_given_status = DataSetup().grab_compliance_list_of_given_status(self.status)
        self.sorted_api_compliance_list_by_resource_of_given_status = sorted(
            api_compliance_list_by_resource_of_given_status, key=itemgetter('name', 'key', 'status'))
        self.sort_option = 'Requirement'

        api_compliance_list_by_resources_sorted_by_given_option = DataSetup().grab_compliance_list_sorted_by_key(
            self.sort_option)
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

        menu_navigation_page.click_on_menu_item('Compliance')

        compliance_page = CompliancePage(self.browser)
        compliance_page.scroll_until_all_compliance_are_visible(len(self.api_sorted_compliance_dictionary))
        aplication_compliance_list = compliance_page.create_list_of_dictionary_for_compliance()

        aplication_sorted_compliance_dictionary = sorted(aplication_compliance_list,
                                                         key=itemgetter('name', 'key', 'status'))

        SoftAssert().verfy_equals_true(
            "List of compliance grabbed from API doesn't matches with the one grabbed from UI ",
            self.api_sorted_compliance_dictionary,
            aplication_sorted_compliance_dictionary)

        compliance_page.select_status(self.status)

        compliance_page.scroll_until_all_compliance_are_visible(
            len(self.sorted_api_compliance_list_by_resource_of_given_status))
        aplication_compliance_filter_list_dictionary = compliance_page.create_list_of_dictionary_for_compliance()
        aplication_compliance_filter_list_dictionary_sorted = sorted(aplication_compliance_filter_list_dictionary,
                                                                     key=itemgetter('name', 'key', 'status'))

        SoftAssert().verfy_equals_true(
            "List of compliance, filter by status, grabbed from API and doesn't matches with the one grabbed from UI ",
            self.sorted_api_compliance_list_by_resource_of_given_status,
            aplication_compliance_filter_list_dictionary_sorted)

        compliance_page.select_status('All')
        compliance_page.select_sort_option(self.sort_option)

        compliance_page.scroll_until_all_compliance_are_visible(
            len(self.sorted_api_compliance_list_by_resources_sorted_by_given_option))
        aplication_compliance_list_dictionary_sort = compliance_page.create_list_of_dictionary_for_compliance()

        SoftAssert().verfy_equals_true(
            "List of compliance, sorted, grabbed from API and doesn't matches with the one grabbed from UI ",
            self.sorted_api_compliance_list_by_resources_sorted_by_given_option,
            aplication_compliance_list_dictionary_sort)

        compliance_page.select_sort_order('descending')
        compliance_page.scroll_until_all_compliance_are_visible(
            len(self.sorted_api_compliance_list_by_resources_sorted_ordered_by_given_option))
        aplication_compliance_list_dictionary_sort_order = compliance_page.create_list_of_dictionary_for_compliance()

        SoftAssert().verfy_equals_true(
            "List of compliance, sorted,ordered, grabbed from API and doesn't matches with the one grabbed from UI ",
            self.sorted_api_compliance_list_by_resources_sorted_ordered_by_given_option,
            aplication_compliance_list_dictionary_sort_order)

        self.assertEqual(SoftAssert().failures_size(), 0, str(SoftAssert().failures_list()))

    def tearDown(self):
        menuNavigationPage = MenuNavigationPage(self.browser)
        menuNavigationPage.close_driver()
