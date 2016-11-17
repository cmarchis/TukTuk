import unittest

from pages.MenuNavigationPage import MenuNavigationPage
from pages.compliance.CompliancePage import CompliancePage
from pages.compliance.ComplianceRuleDetailsPage import ComplianceRuleDetailsPage
from pages.templates.TemplatesMenuListPage import TemplatesMenuListPage
from pages.templates.details.TemplateDetailsPage import TemplateDetailsPage
from pages.deployments.DeploymentsPage import DeploymentsPage
from pages.LoginPage import LoginPage
from pages.LandingPage import LandingPage
from tools.ConfigUtils import ConfigUtils
from tools.DriverUtils import DriverUtils
from tools.SoftAssert import SoftAssert
from tools.api.mock.DataSetup import DataSetup


class ViewRuleDetailsTest(unittest.TestCase):
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

        self.random_template_id = DataSetup().get_random_template_id()
        self.random_deployment_id = DataSetup().grab_random_deployment_by_template_id(self.random_template_id)
        self.random_resource_id = DataSetup().grab_random_resource_id_by_deployment_id(self.random_deployment_id)
        self.random_compliance_id = DataSetup().grab_random_compliance_id_by_resource_id(self.random_resource_id)
        self.compliance_details = DataSetup().grab_compliance_details(self.random_resource_id,
                                                                      self.random_compliance_id)

        self.number_of_compliance = DataSetup().get_number_of_compliance(self.random_resource_id)

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
        menu_navigation_page = MenuNavigationPage(self.browser)
        menu_navigation_page.click_on_menu_item('Compliance')
        compliance_page = CompliancePage(self.browser)

        compliance_page.scroll_until_all_compliance_are_visible(self.number_of_compliance)
        compliance_page.scroll_to_home()

        compliance_page.click_compliance_by_id(self.random_compliance_id)

        compliance_rule_details_page = ComplianceRuleDetailsPage(self.browser)
        aplication_compliance_rule_details = compliance_rule_details_page.create_compliance_rule_details_list_of_dictionary()

        SoftAssert().verfy_equals_true(
            "Details compliance information doesn't matched with information grabbed from API ",
            self.compliance_details, aplication_compliance_rule_details)

        self.assertEqual(SoftAssert().failures_size(), 0, str(SoftAssert().failures_list()))

    def tearDown(self):
        menuNavigationPage = MenuNavigationPage(self.browser)
        menuNavigationPage.close_driver()
