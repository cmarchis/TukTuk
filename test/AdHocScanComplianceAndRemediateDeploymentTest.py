import unittest

from pages.MenuNavigationPage import MenuNavigationPage
from pages.templates.TemplatesMenuListPage import TemplatesMenuListPage
from pages.templates.details.TemplateDetailsPage import TemplateDetailsPage
from pages.deployments.DeploymentsMenuHeaderPage import DeploymentsMenuHeaderPage
from pages.deployments.DeploymentsPage import DeploymentsPage

from tools.DriverUtils import DriverUtils
from tools.SoftAssert import SoftAssert


class AdHocScanComplianceAndRemediateDeploymentTest(unittest.TestCase):
    def setUp(self):
        self.expected_scan_message = 'SCAN in progress'
        self.browser = DriverUtils().start_driver()

    def test_AdHocScanComplianceAndRemediateDeploymentTest(self):
        menu_navigation_page = MenuNavigationPage(self.browser)
        menu_navigation_page.navigate_to("http://localhost:8014/provision")
        menu_navigation_page.navigate_to("http://localhost:8014/provision")
        templates_menu_list_page = TemplatesMenuListPage(self.browser)
        templates_menu_list_page.click_on_template_item("5 - Windows Server")

        template_details_page = TemplateDetailsPage(self.browser)
        template_details_page.select_deployment('5 - Sample Deployment')

        deployment_menu_header_page = DeploymentsMenuHeaderPage(self.browser)
        deployment_menu_header_page.click_on_header_menu_item("Scan Compliance")
        deployment_menu_header_page.get_menu_option_state()



        # deployment_page = DeploymentsPage(self.browser)
        # aplication_notification_message = deployment_page.get_notification_message()
        #
        # SoftAssert().verfy_equals_true("Scan message isn't being displayed properly",
        #                                self.expected_scan_message, aplication_notification_message)
        #
        # deployment_menu_header_page.click_on_header_menu_item("Remediate")
        # aplication_notification_message = deployment_page.get_notification_message()
        # SoftAssert().verfy_equals_true("Remediate message isn't being displayed properly",
        #                                self.expected_scan_message, aplication_notification_message)

        self.assertEqual(SoftAssert().failures_size(), 0, str(SoftAssert().failures_list()))

    def tearDown(self):
        menuNavigationPage = MenuNavigationPage(self.browser)
        menuNavigationPage.close_driver()
