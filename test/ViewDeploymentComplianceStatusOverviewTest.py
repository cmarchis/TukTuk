import unittest

from pages.MenuNavigationPage import MenuNavigationPage
from pages.deployments.DeploymentsPage import DeploymentsPage
from tools import ListUtils, ApiUtils
from tools.ApiUtils import ApiUtils
from tools.DriverUtils import DriverUtils
from tools.ListUtils import ListUtils
from tools.SoftAssert import SoftAssert


class ViewDeploymentComplianceStatusOverviewTest(unittest.TestCase):
    def setUp(self):
        self.policies_list = ApiUtils().grab_policies_json()
        api_policy_types_list = ListUtils().grab_list_of_policies_types(self.policies_list)
        no_duplicate_policy_list = ListUtils().remove_duplicates_from_list(api_policy_types_list)
        policies_model_list = ListUtils().create_list_of_policies_model(self.policies_list)
        self.api_policies_list = ListUtils().sort_list_alphabetically_by('type', policies_model_list)
        self.api_resource_list_with_status = ListUtils().sort_list_alphabetically_by('name',
                                                                                     ListUtils().grab_list_of_resources_with_status(
                                                                                         self.policies_list))

        self.browser = DriverUtils().start_driver()

    def test_ViewDeploymentComplianceStatusOverviewTest(self):
        menu_navigation_page = MenuNavigationPage(self.browser)
        menu_navigation_page.navigate_to("http://localhost:8014/provision")
        menu_navigation_page.navigate_to("http://localhost:8014/provision")
        menu_navigation_page.click_on_menu_item("Deployments")
        deployment_page = DeploymentsPage(self.browser)
        aplication_policies_list = ListUtils().sort_list_alphabetically_by('type',
                                                                           deployment_page.create_list_of_dictionary_for_policies())

        SoftAssert().verfy_equals_true("List of policies doesn't matched ",
                                       aplication_policies_list, self.api_policies_list)

        aplication_resources_list_with_status = ListUtils().sort_list_alphabetically_by('name',
                                                                                        deployment_page.create_list_of_dictionary_for_resources())

        SoftAssert().verfy_equals_true("List of resources doesn't matched ",
                                       aplication_resources_list_with_status, self.api_resource_list_with_status)

        self.assertEqual(SoftAssert().failures_size(), 0, str(SoftAssert().failures_list()))

    def tearDown(self):
        menuNavigationPage = MenuNavigationPage(self.browser)
        menuNavigationPage.close_driver()
