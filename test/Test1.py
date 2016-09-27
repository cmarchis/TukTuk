import unittest
from tools.DriverUtils import DriverUtils
from tools.WebdriverBase import WebdriverBase
from pages.MenuNavigationPage import MenuNavigationPage
from pages.DeploymentsMenuHeaderPage import DeploymentsMenuHeaderPage



class Test1(unittest.TestCase):
    def setUp(self):
        self.browser = DriverUtils().start_driver()

    def test_Test1(self):
        menu_navigation_page=MenuNavigationPage(self.browser)
        menu_navigation_page.navigate_to("http://172.22.140.63:8014/provision")
        menu_navigation_page.navigate_to("http://172.22.140.63:8014/provision")
        menu_navigation_page.click_on_menu_item("Deployments")
        deployments_menu_header_page=DeploymentsMenuHeaderPage(self.browser)
        deployments_menu_header_page.click_on_header_menu_item("Scan Compliance")



    def tearDown(self):
        menuNavigationPage = MenuNavigationPage(self.browser)
        menuNavigationPage.close_driver()