import unittest
from tools.DriverUtils import DriverUtils
from pages.MenuNavigationPage import MenuNavigationPage
from pages.DeploymentsPage import DeploymentsPage
from tools.ListUtils import ListUtils
from tools.ApiUtils import ApiUtils
from tools.SoftAssert import SoftAssert


class Test1(unittest.TestCase):
    def setUp(self):
        self.api_policies_list = ListUtils().sort_list_alpahbetic(ListUtils().create_list_of_policies_model(
            ListUtils().remove_duplicates_from_list(ApiUtils().grab_list_of_policies_types())))
        self.api_resource_list_with_status = ListUtils().sort_list_alpahbetic_by_name(
            ApiUtils().grab_list_of_resources_with_status())

        self.browser = DriverUtils().start_driver()

    def test_Test1(self):
        menu_navigation_page = MenuNavigationPage(self.browser)
        menu_navigation_page.navigate_to("http://localhost:8014/provision")
        menu_navigation_page.navigate_to("http://localhost:8014/provision")
        menu_navigation_page.click_on_menu_item("Deployments")
        deployment_page = DeploymentsPage(self.browser)
        aplication_policies_list = ListUtils().sort_list_alpahbetic(
            deployment_page.create_list_of_dictionary_for_policies())

        SoftAssert().verfy_equals_true("List of policies doesn't matched ",
                                       aplication_policies_list, self.api_policies_list)

        aplication_resources_list_with_status = ListUtils().sort_list_alpahbetic_by_name(
            deployment_page.create_list_of_dictionary_for_resources())

        SoftAssert().verfy_equals_true("List of resources doesn't matched ",
                                       aplication_resources_list_with_status, self.api_resource_list_with_status)

        self.assertEqual(SoftAssert().failures_size(), 0, str(SoftAssert().failures_list()))

    def tearDown(self):
        menuNavigationPage = MenuNavigationPage(self.browser)
        menuNavigationPage.close_driver()
