from tools.WebdriverBase import WebdriverBase

COMPLIANCE_LIST_SELECTOR = 'ul.grommetux-list--selectable li'
RESOURCE_INFO_LIST_SELECTOR = 'div.grommetux-box--pad-small>div:first-child>div'
ADD_EDIT_CREDENTIAL_BUTTON_SELECTOR = 'li button.grommetux-button--icon span.grommetux-button__icon'
CREDENTIAL_LIST_SELECTOR = 'div.grommetux-box--pad-vertical-medium ul li.grommetux-box--pad-medium span'


class ResourceDetailsPage(WebdriverBase):
    """
    Actions related to Resources Details page
    """

    def grab_compliance_dictionary_list(self):
        result_list = []
        compliance_rows = self.locate_elements_by_css_selector(COMPLIANCE_LIST_SELECTOR)
        for row_now in compliance_rows:
            compliance_data = {}
            compliance_data['id'] = row_now.get_attribute('id')
            compliance_data['name'] = row_now.find_element_by_css_selector('div:first-child label').text
            compliance_data['status'] = row_now.find_element_by_css_selector('div:last-child').text
            result_list.append(compliance_data)
        return result_list

    def select_compliance_by_compliance_id(self, compliance_id):
        compliance_list = self.locate_elements_by_css_selector(COMPLIANCE_LIST_SELECTOR)
        for compliance in compliance_list:
            if compliance.get_attribute('id') == compliance_id:
                compliance.click()
                break

    def grab_resource_info(self):
        resource_data = {}
        resource_info_list = self.locate_elements_by_css_selector(RESOURCE_INFO_LIST_SELECTOR)
        for resource in resource_info_list:
            if resource.find_element_by_css_selector('div:first-child').text == 'Template':
                resource_data['template'] = resource.find_element_by_css_selector('div:last-child').text
            elif resource.find_element_by_css_selector('div:first-child').text == 'Deployment':
                resource_data['deployment'] = resource.find_element_by_css_selector('div:last-child').text
            elif resource.find_element_by_css_selector('div:first-child').text == 'Compliance':
                resource_data['compliance'] = resource.find_element_by_css_selector('div:last-child').text
        return resource_data

    def grab_credentials_list(self):
        element_list = self.locate_elements_by_css_selector(CREDENTIAL_LIST_SELECTOR)
        credential_list = []
        for credential in element_list:
            credential_list.append(credential.text)
        return credential_list

    def click_credential_add_edit_button(self):
        add_edit_button = self.locate_element_by_css_selector(ADD_EDIT_CREDENTIAL_BUTTON_SELECTOR)
        add_edit_button.click()


