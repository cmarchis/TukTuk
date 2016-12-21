import unittest

from pages.MenuNavigationPage import MenuNavigationPage
from pages.LoginPage import LoginPage
from pages.LandingPage import LandingPage
from pages.resources.ResourcesPage import ResourcesPage
from pages.resources.ResourceDetailsPage import ResourceDetailsPage
from pages.resources.SelectCredentialPage import SelectCredentialPage
from tools.DriverUtils import DriverUtils
from tools.SoftAssert import SoftAssert
from tools.ConfigUtils import ConfigUtils
from tools.dataSetup.ResourceDataSetup import ResourceDataSetup


class ViewComplianceResultsInResourcesDetailsTest(unittest.TestCase):
    """
    Test contain 1 verification steps:
        - is verifying that the assigned credential is displayed in resource details page

    In te setUp phase is grabbed:
        - a random resource id

    Test:
        - is navigating to Resources page
        - is selecting a resource by it's id
        - is clicking on add/edit credentials button from details resources page
        - is selecting a credential from drop down selector from select credential layer
        - is clicking the save button
        - is verifying that the assigned credential is displayed in resource details page
    """

    def setUp(self):
        self.base_url = ConfigUtils().read_config_file()['baseURL']
        self.user_name = ConfigUtils().read_config_file()['userName']
        self.user_pass = ConfigUtils().read_config_file()['userPass']
        self.api_url = ConfigUtils().read_config_file()['apiBaseURL']

        self.random_resource_id = ResourceDataSetup().grab_random_resouce_id()

        self.browser = DriverUtils().start_driver()

    def test_ViewTemplatesTest(self):
        menu_navigation_page = MenuNavigationPage(self.browser)
        menu_navigation_page.navigate_to(self.base_url)

        login_page = LoginPage(self.browser)
        login_page.perform_login(self.user_name, self.user_pass)

        landing_page = LandingPage(self.browser)
        landing_page.select_resource_management_from_menu()
        menu_navigation_page.click_on_menu_item("Resources")

        resource_page = ResourcesPage(self.browser)
        resource_page.select_resource_by_resource_id(self.random_resource_id)

        resource_details_page = ResourceDetailsPage(self.browser)
        resource_details_page.click_credential_add_edit_button()

        select_credential_page = SelectCredentialPage(self.browser)
        select_credential_page.click_select_credential_drop_down()
        random_credential = select_credential_page.grab_random_credential()
        select_credential_page.select_credential(random_credential)
        select_credential_page.click_save_button()

        credentials_list = resource_details_page.grab_credentials_list()

        api_credential_list = ResourceDataSetup().grab_credential_list_for_resource_id(self.random_resource_id)

        SoftAssert().verfy_equals_true(
            "Credentials list grabbed from API doesn't matched with the list grabbed from UI",
            api_credential_list, credentials_list)

        self.assertEqual(SoftAssert().failures_size(), 0, str(SoftAssert().failures_list()))

    def tearDown(self):
        menuNavigationPage = MenuNavigationPage(self.browser)
        menuNavigationPage.close_driver()
