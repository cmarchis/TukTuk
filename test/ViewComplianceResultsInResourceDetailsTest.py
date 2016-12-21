import unittest

from pages.MenuNavigationPage import MenuNavigationPage
from pages.LoginPage import LoginPage
from pages.LandingPage import LandingPage
from pages.resources.ResourcesPage import ResourcesPage
from pages.resources.ResourceDetailsPage import ResourceDetailsPage
from pages.resources.ResourceComplianceDetailsPage import ResourceComplianceDetailsPage
from tools.DriverUtils import DriverUtils
from tools.SoftAssert import SoftAssert
from tools.ConfigUtils import ConfigUtils
from tools.dataSetup.ResourceDataSetup import ResourceDataSetup


class ViewComplianceResultsInResourceDetailsTest(unittest.TestCase):
    """
    Test contain 3 verification steps:
        - is validating that the resource details list grabbed form API matches with the grabbed list from UI
        - is validating that the dictionary list of compliance grabbed from API matches with the grabbed list from UI
        - is validating that the dictionary list of compliance details grabbed from API matches with the grabbed list
        from UI

    In te setUp phase is grabbed:
        - a random resource id
        - the list of compliance for the random resource id
        - a random compliance id
        - a list of resource compliance details data
        - a list containing resource information

    Test:
        - is navigating to Resources page
        - is selecting a resource by it's id
        - is grabbing the resource details information
        - is validating that the resource details list grabbed form API matches with the grabbed list from UI
        - is grabbing the dictionary list of compliance
        - is validating that the dictionary list of compliance grabbed from API matches with the grabbed list from UI
        - is selecting a compliance by it's id
        - is grabbing compliance dictionary list
        - is validating that the dictionary list of compliance details grabbed from API matches with the grabbed list
        from UI
    """

    def setUp(self):
        self.base_url = ConfigUtils().read_config_file()['baseURL']
        self.user_name = ConfigUtils().read_config_file()['userName']
        self.user_pass = ConfigUtils().read_config_file()['userPass']
        self.api_url = ConfigUtils().read_config_file()['apiBaseURL']

        self.random_resource_id = ResourceDataSetup().grab_random_resouce_id()
        self.resource_compliance_list_for_resource = ResourceDataSetup().grab_compliance_list_for_resource_id(
            self.random_resource_id)

        self.random_compliance_id = ResourceDataSetup().grab_random_compliance_id_from_resouce_compliance_list(
            self.resource_compliance_list_for_resource)

        self.resource_compliance_details_data = ResourceDataSetup().grab_resource_compliance_details_data(
            self.random_resource_id, self.random_compliance_id)

        self.api_resource_info = ResourceDataSetup().grab_resource_info(self.random_resource_id)

        self.browser = DriverUtils().start_driver()

    def test_ViewTemplatesTest(self):
        menu_navigation_page = MenuNavigationPage(self.browser)
        menu_navigation_page.navigate_to(self.base_url)
        menu_navigation_page.navigate_to(self.base_url)

        login_page = LoginPage(self.browser)
        login_page.perform_login(self.user_name, self.user_pass)

        landing_page = LandingPage(self.browser)
        landing_page.select_resource_management_from_menu()
        menu_navigation_page.click_on_menu_item("Resources")

        resource_page = ResourcesPage(self.browser)
        resource_page.select_resource_by_resource_id(self.random_resource_id)

        resource_details_page = ResourceDetailsPage(self.browser)
        resource_info = resource_details_page.grab_resource_info()

        SoftAssert().verfy_equals_true(
            "Resource info list grabbed from API doesn't matched with the list grabbed from UI",
            self.api_resource_info, resource_info)

        resource_compliance_list = resource_details_page.grab_compliance_dictionary_list()

        SoftAssert().verfy_equals_true(
            "Resource compliance list grabbed from API doesn't matched with the list grabbed from UI",
            self.resource_compliance_list_for_resource, resource_compliance_list)

        resource_details_page.select_compliance_by_compliance_id(self.random_compliance_id)
        resource_compliance_details_page = ResourceComplianceDetailsPage(self.browser)

        resource_compliance_details_dictionary_list = \
            resource_compliance_details_page.grab_resource_compliance_details_dictionary_list()

        SoftAssert().verfy_equals_true(
            "Resource compliance details list grabbed from API doesn't matched with the list grabbed from UI",
            self.resource_compliance_details_data, resource_compliance_details_dictionary_list)

        self.assertEqual(SoftAssert().failures_size(), 0, str(SoftAssert().failures_list()))

    def tearDown(self):
        menuNavigationPage = MenuNavigationPage(self.browser)
        menuNavigationPage.close_driver()
