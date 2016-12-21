import unittest

from pages.MenuNavigationPage import MenuNavigationPage
from pages.LoginPage import LoginPage
from pages.LandingPage import LandingPage
from pages.controls.ControlsPage import ControlsPage
from tools.DriverUtils import DriverUtils
from tools.SoftAssert import SoftAssert
from tools.ConfigUtils import ConfigUtils
from tools.dataSetup.ControlsDataSetup import ControlsDataSetup
from tools.ListUtils import ListUtils


class ViewControlTest(unittest.TestCase):
    """
    Test contain 3 verification steps:
    - is verifying that the list of controls grabbed from UI matches with the list grabbed from API
    - is verifying that the list of controls sorted by name ascending grabbed from UI matches with the list grabbed
    from API
    - is verifying that the list of controls sorted by name descending grabbed from UI matches with the list grabbed
    from API

    In te setUp phase is grabbed:
    - a dictionary list of controls grabbed from API
    - a dictionary list of controls sorted by name ascending
    - a dictionary list of controls sorted by name descending

    Test:
    - is navigating to Controls page
    - is scrolling until all controls are displayed
    - is grabbing the dictionary list of all controls that are displayed
    - is sorting ascending the grabbed list by id key
    - is verifying that the list of controls grabbed from UI matches with the list grabbed from API
    - is selecting from filter layer the Name sorting option
    - is scrolling until all controls are displayed
    - is grabbing the dictionary list of all controls that are displayed
    - is verifying that the list of controls sorted by name ascending grabbed from UI matches with the list grabbed
    from API
    - is selecting from filter layer the descending sorting option
    - is scrolling until all controls are displayed
    - is grabbing the dictionary list of all controls that are displayed
    - is verifying that the list of controls sorted by name descending grabbed from UI matches with the list grabbed
    from API
    """

    def setUp(self):
        self.base_url = ConfigUtils().read_config_file()['baseURL']
        self.user_name = ConfigUtils().read_config_file()['userName']
        self.user_pass = ConfigUtils().read_config_file()['userPass']
        self.api_url = ConfigUtils().read_config_file()['apiBaseURL']

        self.api_control_list = ControlsDataSetup().grab_controls_list()
        self.api_control_list_ascending_order = ControlsDataSetup().grab_controls_name_list_ascending_order()
        self.api_control_list_descending_order = ControlsDataSetup().grab_controls_name_list_descending_order()
        self.number_of_controls = len(self.api_control_list)
        self.expected_list_macthes = True

        self.browser = DriverUtils().start_driver()

    def test_ViewControlTest(self):
        menu_navigation_page = MenuNavigationPage(self.browser)
        menu_navigation_page.navigate_to(self.base_url)
        menu_navigation_page.navigate_to(self.base_url)

        login_page = LoginPage(self.browser)
        login_page.perform_login(self.user_name, self.user_pass)

        landing_page = LandingPage(self.browser)
        landing_page.select_author_from_menu()

        menu_navigation_page.click_on_menu_item('Controls')

        controls_page = ControlsPage(self.browser)
        controls_page.scroll_until_all_controls_are_visible(self.number_of_controls)
        ui_control_list = controls_page.grab_controls_dictionary_list()

        id_sorted_ui_control_list = ListUtils().sort_list_dictionary_natural_ascending_by_key('id', ui_control_list)
        id_sorted_api_control_list = ListUtils().sort_list_dictionary_natural_ascending_by_key('id',
                                                                                               self.api_control_list)
        SoftAssert().verfy_equals_true(
            "Controls list grabbed from API doesn't matched with list grabbed from UI",
            id_sorted_api_control_list, id_sorted_ui_control_list)

        controls_page.select_sorting_type('Name')
        controls_page.scroll_until_all_controls_are_visible(self.number_of_controls)
        ui_name_control_list_ascending = controls_page.grab_name_controls_dictionary_list()

        SoftAssert().verfy_equals_true(
            "Controls name list ordered ascending grabbed from API doesn't matched with list grabbed from UI",
            self.api_control_list_ascending_order, ui_name_control_list_ascending)

        controls_page.select_descending_sorting()
        controls_page.scroll_until_all_controls_are_visible(self.number_of_controls)
        ui_name_control_list_descending = controls_page.grab_name_controls_dictionary_list()

        SoftAssert().verfy_equals_true(
            "Controls name list ordered descending grabbed from API doesn't matched with list grabbed from UI",
            self.api_control_list_descending_order, ui_name_control_list_descending)

        self.assertEqual(SoftAssert().failures_size(), 0, str(SoftAssert().failures_list()))

    def tearDown(self):
        menuNavigationPage = MenuNavigationPage(self.browser)
        menuNavigationPage.close_driver()
