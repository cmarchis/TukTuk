from tools.WebdriverBase import WebdriverBase
import time

NAME_INPUT_SELECTOR = 'input#name'
USERNAME_INPUT_SELECTOR = 'input#username'
PASSWORD_INPUT_SELECTOR = 'input#password'
CONFIRM_PASSWORD_INPUT_SELECTOR = 'input#confirmPassword'
SAVE_BUTTON_SELECTOR = 'footer button.grommetux-button'
LABEL_LIST_SELECTOR = 'div.grommetux-form-field--size-medium'
CLOSE_BUTTON = 'div.grommetux-layer__closer svg.grommetux-control-icon-close'


class AddCredentialPage(WebdriverBase):
    def add_name(self, new_name):
        name = self.locate_element_by_css_selector(NAME_INPUT_SELECTOR)
        name.send_keys(new_name)

    def add_username(self, new_username):
        name = self.locate_element_by_css_selector(USERNAME_INPUT_SELECTOR)
        name.send_keys(new_username)

    def add_password(self, new_password):
        name = self.locate_element_by_css_selector(PASSWORD_INPUT_SELECTOR)
        name.send_keys(new_password)

    def confirm_password(self, new_password):
        name = self.locate_element_by_css_selector(CONFIRM_PASSWORD_INPUT_SELECTOR)
        name.send_keys(new_password)

    def click_save_button(self):
        save_button = self.locate_element_by_css_selector(SAVE_BUTTON_SELECTOR)
        save_button.click()
        time.sleep(3)

    def add_credential(self, new_name, new_username, new_password):
        self.add_name(new_name)
        self.add_username(new_username)
        self.add_password(new_password)
        self.confirm_password(new_password)

    def verify_form_field_error_message(self, input_field, field_error_message):
        boolean = False
        label_list = self.locate_elements_by_css_selector(LABEL_LIST_SELECTOR)
        for label in label_list:
            if label.find_element_by_css_selector('label').text == input_field:
                if label.find_element_by_css_selector('span.grommetux-form-field__error').text == field_error_message:
                    boolean = True
        return boolean

    def click_close_add_credential(self):
        close_button = self.locate_element_by_css_selector(CLOSE_BUTTON)
        close_button.click()
