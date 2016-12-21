from tools.WebdriverBase import WebdriverBase

RESOURCES_LIST_SELECTOR = 'div.grommetux-tiles div'


class ResourcesPage(WebdriverBase):
    """
    Actions related to Resources page
    """

    def grab_resources_dictionary_list(self):
        result_list = []
        resources_rows = self.locate_elements_by_css_selector(RESOURCES_LIST_SELECTOR)
        for row_now in resources_rows:
            policy_data = {}
            policy_data['id'] = row_now.get_attribute('id')
            policy_data['name'] = row_now.find_element_by_css_selector('label:first-child strong').text
            policy_data['template'] = row_now.find_element_by_css_selector('label:last-child').text
            result_list.append(policy_data)
        return result_list

    def select_resource_by_resource_id(self, resource_id):
        resources_list = self.locate_elements_by_css_selector(RESOURCES_LIST_SELECTOR)
        for resource in resources_list:
            if resource.get_attribute('aria-label') == resource_id:
                resource.click()
                break
