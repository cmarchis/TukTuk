import unittest

from pages.MenuNavigationPage import MenuNavigationPage
from pages.compliance.CompliancePage import CompliancePage
from tools.DriverUtils import DriverUtils


class ViewDeploymentComplianceStatusOverviewTest(unittest.TestCase):
    def setUp(self):
        self.browser = DriverUtils().start_driver()

    def test_ViewDeploymentComplianceStatusOverviewTest(self):
        menu_navigation_page = MenuNavigationPage(self.browser)
        menu_navigation_page.navigate_to("http://localhost:8014/provision")
        menu_navigation_page.navigate_to("http://localhost:8014/provision")
        menu_navigation_page.click_on_menu_item("Compliance")
        compliance_page = CompliancePage(self.browser)
        compliance_list = compliance_page.create_list_of_dictionary_for_resources()
        print "copliance_list", compliance_list
        compliance_page.select_sorting_option('Status','Ascending')

    def tearDown(self):
        menuNavigationPage = MenuNavigationPage(self.browser)
        menuNavigationPage.close_driver()
