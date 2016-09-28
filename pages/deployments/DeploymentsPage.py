from tools.WebdriverBase import WebdriverBase

RESOURCES_LIST_SELECTOR = 'li[role="listitem"]:not(.grommetux-box--pad-between-small)'
POLICIES_LIST_SELECTOR = 'div.grommetux-box--pad-small div.grommetux-box--pad-medium:nth-child(2) div.grommetux-box--direction-row:not(.grommetux-box--justify-between)'


class DeploymentsPage(WebdriverBase):
    """
    Mapping for Deployments Tab
    """
    def create_list_of_dictionary_for_resources(self):
        """
        list of dictionary resources. Functionality corresponding to list of resources displayed under the overview.
        :return: list[item{name, status},...]
        """
        resources_list = self.locate_elements_by_css_selector(RESOURCES_LIST_SELECTOR)
        return_list = []
        for item_now in resources_list:
            list_item = {}
            list_item['name'] = item_now.find_element_by_css_selector("div:first-child").text
            list_item['status'] = item_now.find_element_by_css_selector("div:last-child").text
            return_list.append(list_item)
        return return_list

    def create_list_of_dictionary_for_policies(self):
        """
        list of dictionary policies. Functionality corresponding to Compliance status overview Graphics.
        :return: list[item{type, number, variances},...]
        """
        policies_list = self.locate_elements_by_css_selector(POLICIES_LIST_SELECTOR)
        return_list = []
        for item_now in policies_list:
            list_item = {}
            list_item['type'] = item_now.find_element_by_css_selector("div label").text
            list_item['number'] = item_now.find_element_by_css_selector("div h5 span").text
            list_item['variances'] = item_now.find_element_by_css_selector("div h6 span").text
            return_list.append(list_item)
        return return_list

