from tools.WebdriverBase import WebdriverBase

COMPLIANCE_RULE_DETAILS_CONTAINER = 'div.grommetux-box--basis-large'


class ComplianceRuleDetailsPage(WebdriverBase):
    def __init__(self, driver):
        self.driver = driver

    def create_compliance_rule_details_list_of_dictionary(self):
        compliance_container = self.locate_element_by_css_selector(COMPLIANCE_RULE_DETAILS_CONTAINER)
        compliance_rule = {}
        compliance_rule['compliance_name'] = compliance_container.find_element_by_css_selector('header h3').text
        compliance_rule['compliance_status'] = compliance_container.find_element_by_css_selector('div h3').text
        # compliance_rule['compliance_date'] = compliance_container.find_element_by_css_selector('div h5 span').text
        compliance_rule['compliance_policy'] = compliance_container.find_element_by_css_selector(
            'section:nth-child(3) label').text
        compliance_rule['compliance_requirement'] = compliance_container.find_element_by_css_selector(
            'section:nth-child(4) label').text
        compliance_rule['compliance_control'] = compliance_container.find_element_by_css_selector(
            'section:nth-child(5) label').text
        return compliance_rule
