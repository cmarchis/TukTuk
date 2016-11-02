from tools.WebdriverBase import WebdriverBase

USERNAME_SELECTOR = 'input#username'
PASSWORD_SELECTOR = 'input#password'
LOGIN_BUTTON_SELECTPR = 'input#submit'


class LoginPage(WebdriverBase):
    def perform_login(self, user_name, user_pass):
        """
        Perform login with user_name and password. Will also click on submit button
        :param user_name:
        :param user_pass:
        :return:
        """
        self.input_user_name(user_name)
        self.input_user_pass(user_pass)
        self.click_login_button()

    def input_user_name(self, user_name):
        """
        Input user name in the username field
        :param user_name:
        :return:
        """
        self.locate_element_by_css_selector(USERNAME_SELECTOR).send_keys(user_name)

    def input_user_pass(self, user_pass):
        """
        Input user pass in the password field
        :param user_pass:
        :return:
        """
        self.locate_element_by_css_selector(PASSWORD_SELECTOR).send_keys(user_pass)

    def click_login_button(self):
        """
        Click on login button
        :return:
        """
        submit_button = self.locate_element_by_css_selector(LOGIN_BUTTON_SELECTPR)
        submit_button.click()
