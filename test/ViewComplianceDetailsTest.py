import unittest

from pages.MenuNavigationPage import MenuNavigationPage
from pages.compliance.CompliancePage import CompliancePage
from pages.LoginPage import LoginPage
from pages.LandingPage import LandingPage
from pages.compliance.ComplianceRuleDetailsPage import ComplianceRuleDetailsPage
from tools.DriverUtils import DriverUtils
from tools.SoftAssert import SoftAssert
from tools.ConfigUtils import ConfigUtils
from tools.dataSetup.ComplianceDataSetup import ComplianceDataSetup


class ViewComplianceDetailsTest(unittest.TestCase):
    """
    Test contains 1 verification steps:
    In the setUp phase is grabbed:
       - a random template
       - a random deployment id from random template
       - a random resource id from random deployment
       - a random compliance id from resource
       - compliance details for random compliance
       - total number of compliance for random resource
    Test: - is navigating to the chosen template, deployment, resource and compliance for resource.
            - is scrolling till all the compliance are visible
            - is clicking on the random compliance grabbed in setUp phase
            - is grabbing the details of compliance displayed
            - is VALIDATING that the details grabbed from api matches with the details grabbed from application
    """

    def setUp(self):
        self.base_url = ConfigUtils().read_config_file()['baseURL']
        self.user_name = ConfigUtils().read_config_file()['userName']
        self.user_pass = ConfigUtils().read_config_file()['userPass']
        self.api_url = ConfigUtils().read_config_file()['apiBaseURL']

        self.random_compliace_id = ComplianceDataSetup().grab_random_compliance_id()
        self.compliance_number = ComplianceDataSetup().grab_number_of_compliance()
        self.compliance_details = ComplianceDataSetup().grab_compliance_details(self.random_compliace_id)

        self.browser = DriverUtils().start_driver()

    def test_ViewDeploymentComplianceStatusOverviewTest(self):
        menu_navigation_page = MenuNavigationPage(self.browser)
        menu_navigation_page.navigate_to(self.base_url)
        menu_navigation_page.navigate_to(self.base_url)

        login_page = LoginPage(self.browser)
        login_page.perform_login(self.user_name, self.user_pass)

        landing_page = LandingPage(self.browser)
        landing_page.select_resource_management_from_menu()

        menu_navigation_page.click_on_menu_item('Compliance')
        compliance_page = CompliancePage(self.browser)

        compliance_page.select_compliance_by_id(self.random_compliace_id, self.compliance_number)

        compliance_details_page = ComplianceRuleDetailsPage(self.browser)
        ui_compliance_details_dictionary_list = compliance_details_page.create_compliance_rule_details_list_of_dictionary()

        SoftAssert().verfy_equals_true(
            "Details compliance information doesn't matched with information grabbed from API ",
            self.compliance_details, ui_compliance_details_dictionary_list)

        self.assertEqual(SoftAssert().failures_size(), 0, str(SoftAssert().failures_list()))

    def tearDown(self):
        menuNavigationPage = MenuNavigationPage(self.browser)
        menuNavigationPage.close_driver()
