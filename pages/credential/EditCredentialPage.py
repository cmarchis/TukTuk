from tools.WebdriverBase import WebdriverBase
from selenium.webdriver.common.keys import Keys
import time

NAME_INPUT_SELECTOR = 'input#name'
USERNAME_INPUT_SELECTOR = 'input#username'
PASSWORD_INPUT_SELECTOR = 'input#password'
CONFIRM_PASSWORD_INPUT_SELECTOR = 'input#confirmPassword'
SAVE_BUTTON_SELECTOR = 'footer button.grommetux-button'
LABEL_LIST_SELECTOR = 'div.grommetux-form-field--size-medium'


class EditCredentialPage(WebdriverBase):
    def edit_name(self, new_name):
        name = self.locate_element_by_css_selector(NAME_INPUT_SELECTOR)
        name.clear()
        name.send_keys(new_name)

    def edit_username(self, new_username):
        name = self.locate_element_by_css_selector(USERNAME_INPUT_SELECTOR)
        name.clear()
        name.send_keys(new_username)

    def edit_password(self, new_password):
        name = self.locate_element_by_css_selector(PASSWORD_INPUT_SELECTOR)
        name.clear()
        name.send_keys(new_password)

    def confirm_password(self, new_password):
        name = self.locate_element_by_css_selector(CONFIRM_PASSWORD_INPUT_SELECTOR)
        name.clear()
        name.send_keys(new_password)

    def click_save_button(self):
        save_button = self.locate_element_by_css_selector(SAVE_BUTTON_SELECTOR)
        save_button.click()
        time.sleep(3)

    def grab_credential_dictionary_list(self):
        credential_list = []
        credential = {}
        credential['name'] = self.locate_element_by_css_selector(NAME_INPUT_SELECTOR).get_attribute('value')
        credential['username'] = self.locate_element_by_css_selector(USERNAME_INPUT_SELECTOR).get_attribute('value')
        credential_list.append(credential)
        return credential_list

    def verify_form_field_error_message(self, input_field, field_error_message):
        boolean = False
        label_list = self.locate_elements_by_css_selector(LABEL_LIST_SELECTOR)
        for label in label_list:
            if label.find_element_by_css_selector('label').text == input_field:
                if label.find_element_by_css_selector('span.grommetux-form-field__error').text == field_error_message:
                    boolean = True
        return boolean

    # def clear_name(self):
    #     name = self.locate_element_by_css_selector(NAME_INPUT_SELECTOR)
    #     name.clear()
    #     # self.execute_js('$(\'input#name\').value=\'\';')
    #     self.execute_js('arguments[0].setAttribute("value", "")', name)

    def clear_name(self):
        name = self.locate_element_by_css_selector(NAME_INPUT_SELECTOR)
        value_length = len(name.get_attribute('value'))
        for i in range(0, value_length):
            name.send_keys(Keys.BACKSPACE)

    def clear_password(self):
        name = self.locate_element_by_css_selector(PASSWORD_INPUT_SELECTOR)
        value_length = len(name.get_attribute('value'))
        for i in range(0, value_length):
            name.send_keys(Keys.BACKSPACE)

    def edit_credential(self, new_name, new_username, new_password):
        self.edit_name(new_name)
        self.edit_username(new_username)
        self.edit_password(new_password)
        self.confirm_password(new_password)
