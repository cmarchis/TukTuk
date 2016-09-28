import unittest

from pages.MenuNavigationPage import MenuNavigationPage
from tools.DriverUtils import DriverUtils
from pages.templates.TemplatesMenuListPage import TemplatesMenuListPage


class Test1(unittest.TestCase):
    def setUp(self):
        self.browser = DriverUtils().start_driver()

    def test_Test1(self):
        menu_navigation_page = MenuNavigationPage(self.browser)
        menu_navigation_page.navigate_to("http://localhost:8014/provision")
        menu_navigation_page.navigate_to("http://localhost:8014/provision")

        template_menu = TemplatesMenuListPage(self.browser)
        template_menu.click_on_template_item('MySql Provision Template')


    def tearDown(self):
        menuNavigationPage = MenuNavigationPage(self.browser)
        menuNavigationPage.close_driver()
