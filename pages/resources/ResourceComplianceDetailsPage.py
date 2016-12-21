from tools.WebdriverBase import WebdriverBase

COMPLIANCE_DETAILS_CONTAINER_SELECTOR = 'div.grommetux-layer--flush div.grommetux-layer__container'


class ResourceComplianceDetailsPage(WebdriverBase):
    """
    Actions related to Resources pop up page page
    """

    def grab_resource_compliance_details_dictionary_list(self):
        compliance_container = self.locate_element_by_css_selector(COMPLIANCE_DETAILS_CONTAINER_SELECTOR)
        compliance_data = []
        compliance = {}
        compliance['name'] = compliance_container.find_element_by_css_selector('header h3').text
        compliance['status'] = compliance_container.find_element_by_css_selector('div.grommetux-box div h3').text
        compliance['policy'] = compliance_container.find_element_by_css_selector('section:nth-child(3) label').text
        compliance['requirement'] = compliance_container.find_element_by_css_selector(
            'section:nth-child(4) label').text
        compliance['control'] = compliance_container.find_element_by_css_selector('section:nth-child(5) label').text
        compliance_data.append(compliance)
        return compliance_data
