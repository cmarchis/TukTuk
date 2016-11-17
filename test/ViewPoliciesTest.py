import unittest

from pages.MenuNavigationPage import MenuNavigationPage
from pages.templates.TemplatesMenuListPage import TemplatesMenuListPage
from pages.policies.PoliciesListPage import PoliciesListPage
from pages.LoginPage import LoginPage
from pages.LandingPage import LandingPage
from tools.DriverUtils import DriverUtils
from tools.SoftAssert import SoftAssert
from tools.ConfigUtils import ConfigUtils
from tools.api.mock.DataSetup import DataSetup


class ViewTemplatesTest(unittest.TestCase):

    def setUp(self):
        self.base_url = ConfigUtils().read_config_file()['baseURL']
        self.user_name = ConfigUtils().read_config_file()['userName']
        self.user_pass = ConfigUtils().read_config_file()['userPass']
        self.api_url = ConfigUtils().read_config_file()['apiBaseURL']

        self.policy_data = DataSetup().grab_policy_data()

        self.browser = DriverUtils().start_driver()

    def test_ViewTemplatesTest(self):
        menu_navigation_page = MenuNavigationPage(self.browser)
        menu_navigation_page.navigate_to(self.base_url)
        menu_navigation_page.navigate_to(self.base_url)

        login_page = LoginPage(self.browser)
        login_page.perform_login(self.user_name, self.user_pass)

        landing_page = LandingPage(self.browser)
        landing_page.select_provision()
        menu_navigation_page.click_on_menu_item("Policies")

        policies_page = PoliciesListPage(self.browser)
        policies_data = policies_page.grab_policies_dictionary_list()

        print "from page"
        print policies_data

        print "from json"
        print self.policy_data



    def tearDown(self):
        menuNavigationPage = MenuNavigationPage(self.browser)
        menuNavigationPage.close_driver()