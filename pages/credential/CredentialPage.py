from tools.WebdriverBase import WebdriverBase

ADD_CREDENTIAL_BUTTON_SELECTOR = 'h3.grommetux-heading--strong'
CREDENTIAL_LIST_SELECTOR = 'div.grommetux-tile--hover-border-large'


class CredentialPage(WebdriverBase):
    def add_credential(self):
        add_credential_button = self.locate_element_by_css_selector(ADD_CREDENTIAL_BUTTON_SELECTOR)
        add_credential_button.click()

    def edit_credential(self, credential_id):
        credential_list = self.locate_elements_by_css_selector(CREDENTIAL_LIST_SELECTOR)
        for credential in credential_list:
            if credential.get_attribute('id') == credential_id:
                credential.find_element_by_css_selector('svg.grommetux-control-icon-edit').click()
                break

    def delete_credential(self, credential_name):
        credential_list = self.locate_elements_by_css_selector(CREDENTIAL_LIST_SELECTOR)
        for credential in credential_list:
            if credential.find_element_by_css_selector('div>span').text == credential_name:
                credential.find_element_by_css_selector('grommetux-control-icon-close').click()
                break

    def grab_credential_dictionary_list(self):
        credential_list = self.locate_elements_by_css_selector(CREDENTIAL_LIST_SELECTOR)
        credential_name_list = []
        for credential in credential_list:
            credential_data = {}
            credential_data['id'] = credential.get_attribute('id')
            credential_data['name'] = credential.find_element_by_css_selector('h4').text
            credential_name_list.append(credential_data)
        return credential_name_list

    def verify_delete_credential(self, credential_id):
        found = False
        credential_list = self.locate_elements_by_css_selector(CREDENTIAL_LIST_SELECTOR)
        for credential in credential_list:
            if credential.get_attribute('id') == credential_id:
                found = True
                print "True"
        return found
