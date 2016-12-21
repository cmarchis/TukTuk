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


class CredentialManagementFormFieldErrorTest(unittest.TestCase):
    """
    Test contain 4 verification steps:
        - is verifying that for the specified field is displayed the expected error message in add credential layer
        - is verifying that the expected error message for password field is displayed in add credential layer
        - is verifying that for the specified field is displayed the expected error message in edit credential layer
        - is verifying that the expected error message for confirm password field is displayed in edit credential layer

    In te setUp phase is grabbed:
        - a random credential name from credential list

    Test:
        - is navigating to credential page
        - is clicking on add credential button
        - is clicking on save button from add credential layer
        - is verifying that for the specified field is displayed the expected error message in add credential layer
        - is typing a value in password field
        - is typing another value in confirm password field
        - is clicking on save button
        - is verifying that the expected error message for password field is displayed in add credential layer
        - is clicking on close button from add credential layer
        - is clicking on the edit button from the random credential
        - is clearing the name field from edit credential layer
        - is clicking the save button from edit credential layer
        - is verifying that for the specified field is displayed the expected error message in edit credential layer
        - is clearing the password field from edit credential layer
        - is clicking the save button from edit credential layer
        - is verifying that the expected error message for confirm password field is displayed in edit credential layer
    """

    def setUp(self):
        self.base_url = ConfigUtils().read_config_file()['baseURL']
        self.user_name = ConfigUtils().read_config_file()['userName']
        self.user_pass = ConfigUtils().read_config_file()['userPass']
        self.api_url = ConfigUtils().read_config_file()['apiBaseURL']

        self.field_name = 'Name'
        self.expected_message_no_input = 'Required Field'
        self.expected_message_password = 'Passwords Do Not Match'
        self.expected_status = True

        self.random_credential_id = DataSetup().grab_random_credential_id()
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
        credential_page.add_credential()
        add_credential_page = AddCredentialPage(self.browser)
        add_credential_page.click_save_button()
        add_credential_no_input_message_status = add_credential_page.verify_form_field_error_message(self.field_name,
                                                                                                     self.expected_message_no_input)
        SoftAssert().verfy_equals_true(
            "Expected error message for specified field in add credential page doesn't matched",
            self.expected_status, add_credential_no_input_message_status)

        add_credential_page.add_password('a')
        add_credential_page.confirm_password('b')
        add_credential_page.click_save_button()
        add_credential_password_match_message_status = add_credential_page.verify_form_field_error_message('Password',
                                                                                                           self.expected_message_password)
        SoftAssert().verfy_equals_true(
            "Expected error message for password field in add credential page doesn't matched",
            self.expected_status, add_credential_password_match_message_status)
        add_credential_page.click_close_add_credential()

        credential_page.edit_credential(self.random_credential_id)
        edit_credential_page = EditCredentialPage(self.browser)
        edit_credential_page.clear_name()
        edit_credential_page.click_save_button()
        edit_credential_no_input_message_status = edit_credential_page.verify_form_field_error_message(self.field_name,
                                                                                                       self.expected_message_no_input)

        SoftAssert().verfy_equals_true(
            "Expected error message for specified field in edit credential page doesn't matched",
            self.expected_status, edit_credential_no_input_message_status)

        edit_credential_page.clear_password()
        edit_credential_page.click_save_button()

        edit_credential_password_match_message_status = edit_credential_page.verify_form_field_error_message(
            'Confirm Password',
            self.expected_message_password)

        SoftAssert().verfy_equals_true(
            "Expected error message for confirm password field in edit credential page doesn't matched",
            self.expected_status, edit_credential_password_match_message_status)

        self.assertEqual(SoftAssert().failures_size(), 0, str(SoftAssert().failures_list()))

    def tearDown(self):
        menuNavigationPage = MenuNavigationPage(self.browser)
        menuNavigationPage.close_driver()
