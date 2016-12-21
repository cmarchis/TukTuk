import unittest
from pages.MenuNavigationPage import MenuNavigationPage
from pages.LoginPage import LoginPage
from pages.LandingPage import LandingPage
from pages.credential.CredentialPage import CredentialPage
from pages.credential.EditCredentialPage import EditCredentialPage
from pages.credential.AddCredentialPage import AddCredentialPage
from tools.DriverUtils import DriverUtils
from tools.SoftAssert import SoftAssert
from tools.ConfigUtils import ConfigUtils
from tools.api.mock.DataSetup import DataSetup
from tools.StringUtils import StringUtils


class CredentialManagementScreenTest(unittest.TestCase):
    """
    Test contain 4 verification steps:
        - is verifying that the credential list grabbed from API matches with the grabbed list from UI
        - is verifying that the data grab from API matches with the data grabbed from UI after edit action
        - is verifying that the data grab from API matches with the data grabbed from UI after add action
        - is verifying that the deleted credential is no longer displayed

    In the setUp phase is grabbed:
        - list of credential
        - random credential id

    Test:
        - is navigating to Credential page
        - is grabbing the list of all credential displayed
        - is verifying that the credential list grabbed from API matches with the grabbed list from UI
        - is clicking on the edit button of a random credential
        - is editing the credential name, username, password
        - is grabbing credential details info after edit action
        - is clicking on save button from edit credential layer
        - is making a API call to grab the credential data for the edited credential
        - is verifying that the dictionary list grab from API matches with the dictionary list grabbed from UI after edit action
        - is clicking on the add credential button
        - is creating a new credential by typing name, username, password and confirm password values in the defined fields
        - is grabbing the data from the new credential
        - is clicking on save button from add credential layer
        - is making a API call to grab the credential data for the new credential
        - is verifying that the dictionary list grab from API matches with the dictionary list grabbed from UI after add action
        - is clicking on the edit button of a random credential
        - is clicking remove button from edit credential page
        - is verifying that the deleted credential is no longer displayed
    """

    def setUp(self):
        self.base_url = ConfigUtils().read_config_file()['baseURL']
        self.user_name = ConfigUtils().read_config_file()['userName']
        self.user_pass = ConfigUtils().read_config_file()['userPass']
        self.api_url = ConfigUtils().read_config_file()['apiBaseURL']

        self.grab_dictionary_list_of_credential = DataSetup().grab_credential_data_list()
        self.random_credential_id = DataSetup().grab_random_credential_id()
        edit_random_string_number = StringUtils().generate_random_string_number(999)
        self.edit_name = 'credential' + edit_random_string_number
        self.edit_username = 'username' + edit_random_string_number
        self.edit_password = 'pass' + edit_random_string_number
        add_random_string_number = StringUtils().generate_random_string_number(999)
        self.add_name = 'credential' + add_random_string_number
        self.add_username = 'username' + add_random_string_number
        self.add_password = 'pass' + add_random_string_number

        self.expected_find_after_remove_credential_by_id_status = False

        self.browser = DriverUtils().start_driver()

    def test_ViewTemplatesTest(self):
        menu_navigation_page = MenuNavigationPage(self.browser)
        menu_navigation_page.navigate_to(self.base_url)
        menu_navigation_page.navigate_to(self.base_url)

        login_page = LoginPage(self.browser)
        login_page.perform_login(self.user_name, self.user_pass)

        landing_page = LandingPage(self.browser)
        landing_page.select_settings_from_menu()

        menu_navigation_page.click_on_menu_item('Credential')

        credential_page = CredentialPage(self.browser)
        aplication_credential_dictionary_list = credential_page.grab_credential_dictionary_list()

        SoftAssert().verfy_equals_true("Credential dictionary lists doesn't matched ",
                                       self.grab_dictionary_list_of_credential, aplication_credential_dictionary_list)

        credential_page.edit_credential(self.random_credential_id)
        edit_credential_page = EditCredentialPage(self.browser)
        edit_credential_page.edit_credential(self.edit_name, self.edit_username, self.edit_password)
        aplication_edit_credential_list = edit_credential_page.grab_credential_dictionary_list()
        edit_credential_page.click_save_button()
        edit_credential_list_by_id = DataSetup().grab_credential_data_by_id(self.random_credential_id)

        SoftAssert().verfy_equals_true("Edit credential details data doesn't matched with API grabbed data",
                                       edit_credential_list_by_id, aplication_edit_credential_list)

        credential_page.add_credential()
        add_credential = AddCredentialPage(self.browser)
        add_credential.add_credential(self.add_name, self.add_username, self.add_password)
        aplication_add_credential_list = edit_credential_page.grab_credential_dictionary_list()
        add_credential.click_save_button()

        api_add_credential_list_by_name = DataSetup().grab_credential_data_by_name(self.add_name)

        SoftAssert().verfy_equals_true("Add credential data doesn't matched with API grabbed data",
                                       api_add_credential_list_by_name, aplication_add_credential_list)

        credential_page.edit_credential(self.random_credential_id)
        edit_credential_page = EditCredentialPage(self.browser)
        edit_credential_page.click_remove_button()
        remove_credential_by_id_status = credential_page.verify_delete_credential(self.random_credential_id)

        SoftAssert().verfy_equals_true("Deleted credential was still found in credential list",
                                       self.expected_find_after_remove_credential_by_id_status,
                                       remove_credential_by_id_status)

        self.assertEqual(SoftAssert().failures_size(), 0, str(SoftAssert().failures_list()))

    def tearDown(self):
        menuNavigationPage = MenuNavigationPage(self.browser)
        menuNavigationPage.close_driver()
