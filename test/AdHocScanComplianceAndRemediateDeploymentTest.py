import unittest

from pages.MenuNavigationPage import MenuNavigationPage
from pages.templates.TemplatesMenuListPage import TemplatesMenuListPage
from pages.templates.details.TemplateDetailsPage import TemplateDetailsPage
from pages.deployments.DeploymentsMenuHeaderPage import DeploymentsMenuHeaderPage
from pages.deployments.DeploymentsPage import DeploymentsPage

from tools.DriverUtils import DriverUtils
from tools.SoftAssert import SoftAssert
from tools.ListUtils import ListUtils
from tools.ApiUtils import ApiUtils


class AdHocScanComplianceAndRemediateDeploymentTest(unittest.TestCase):
    def setUp(self):
        self.expected_scan_message = 'SCAN in progress'
        self.expected_remediate_message = 'REMEDIATE in progress'
        self.expected_menu_option_state = 'Disabled'
        self.templtes_json = ApiUtils().grab_templates_json()
        self.list_of_templates = ListUtils().grab_template_names(self.templtes_json)
        self.random_template = ListUtils().return_random_from_list(self.list_of_templates)
        self.deployment_list = ListUtils().grab_deployment_list(self.random_template, self.templtes_json)
        self.random_deployment = ListUtils().return_random_from_list(self.deployment_list)

        self.browser = DriverUtils().start_driver()

    def test_AdHocScanComplianceAndRemediateDeploymentTest(self):
        menu_navigation_page = MenuNavigationPage(self.browser)
        menu_navigation_page.navigate_to("http://localhost:8014/provision")
        menu_navigation_page.navigate_to("http://localhost:8014/provision")
        templates_menu_list_page = TemplatesMenuListPage(self.browser)
        templates_menu_list_page.click_on_template_item(self.random_template)

        template_details_page = TemplateDetailsPage(self.browser)
        template_details_page.select_deployment(self.random_deployment)

        deployment_menu_header_page = DeploymentsMenuHeaderPage(self.browser)
        deployment_menu_header_page.click_on_header_menu_item("Scan Compliance")
        deployment_page = DeploymentsPage(self.browser)

        aplication_notification_message = deployment_page.get_notification_message()

        SoftAssert().verfy_equals_true("Scan message isn't being displayed properly",
                                       self.expected_scan_message, aplication_notification_message)

        aplication_menu_option_state = deployment_menu_header_page.get_menu_option_state()
        SoftAssert().verfy_equals_true("Menu option state isn't as expected",
                                       self.expected_menu_option_state, aplication_menu_option_state)

        deployment_page.wait_until_notification_disappear()

        deployment_menu_header_page.click_on_header_menu_item("Remediate")
        aplication_notification_message = deployment_page.get_notification_message()
        SoftAssert().verfy_equals_true("Remediate message isn't being displayed properly",
                                       self.expected_remediate_message, aplication_notification_message)
        aplication_menu_option_state = deployment_menu_header_page.get_menu_option_state()
        SoftAssert().verfy_equals_true("Menu option state isn't as expected",
                                       self.expected_menu_option_state, aplication_menu_option_state)

        self.assertEqual(SoftAssert().failures_size(), 0, str(SoftAssert().failures_list()))

    def tearDown(self):
        menuNavigationPage = MenuNavigationPage(self.browser)
        menuNavigationPage.close_driver()
