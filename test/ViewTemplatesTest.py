import unittest
import time
from pages.MenuNavigationPage import MenuNavigationPage
from pages.templates.TemplatesMenuListPage import TemplatesMenuListPage
from pages.templates.details.TemplateDetailsPage import TemplateDetailsPage
from pages.templates.details.TemplateActionsPage import TemplatActionsPage
from tools.DriverUtils import DriverUtils


class Test1(unittest.TestCase):
    template_name = 'MySql Provision Template'


    def setUp(self):
        self.browser = DriverUtils().start_driver()

    def test_Test1(self):
        menu_navigation_page = MenuNavigationPage(self.browser)
        menu_navigation_page.navigate_to("http://localhost:8014/provision")
        menu_navigation_page.navigate_to("http://localhost:8014/provision")

        template_menu = TemplatesMenuListPage(self.browser)
        template_menu.click_on_template_item(self.template_name)

        template_details = TemplateDetailsPage(self.browser)

        print template_details.grab_resources_data()
        print template_details.grab_policies_data()
        print template_details.grab_deployments_data()

        template_actions = TemplatActionsPage(self.browser)
        print template_actions.grab_actions_label()
        template_actions.click_deploy()
        time.sleep(5)
        self.browser.back()
        time.sleep(5)
        template_actions.click_schedule()
        time.sleep(5)

    def tearDown(self):
        menuNavigationPage = MenuNavigationPage(self.browser)
        menuNavigationPage.close_driver()
