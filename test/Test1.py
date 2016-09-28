import unittest

from pages.DeploymentsPage import DeploymentsPage

from pages.MenuNavigationPage import MenuNavigationPage
from pages.deployments.DeploymentsMenuHeaderPage import DeploymentsMenuHeaderPage
from tools.DriverUtils import DriverUtils


class Test1(unittest.TestCase):
    def setUp(self):
        self.browser = DriverUtils().start_driver()

    def test_Test1(self):
        menu_navigation_page = MenuNavigationPage(self.browser)
        menu_navigation_page.navigate_to("http://localhost:8014/provision")
        menu_navigation_page.navigate_to("http://localhost:8014/provision")
        menu_navigation_page.click_on_menu_item("Deployments")
        deployments_menu_header_page = DeploymentsMenuHeaderPage(self.browser)
        deployments_menu_header_page.click_on_header_menu_item("Scan Compliance")
        deployment_page = DeploymentsPage(self.browser)
        print "list :", deployment_page.create_list_of_dictionary_for_resources()
        print "list :", deployment_page.create_list_of_dictionary_for_policies()

    def tearDown(self):
        menuNavigationPage = MenuNavigationPage(self.browser)
        menuNavigationPage.close_driver()
