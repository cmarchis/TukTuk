from tools.WebdriverBase import WebdriverBase

RESOURCES_LIST_SELECTOR = 'li[role="listitem"]:not(.grommetux-box--pad-between-small)'
POLICIES_LIST_SELECTOR = 'div.grommetux-box--pad-small div.grommetux-box--pad-medium:nth-child(2) div.grommetux-box--direction-row:not(.grommetux-box--justify-between)'
DEPLOYMENT_INFO_SELECTOR = 'div.grommetux-background-color-index-light-1 div.grommetux-box--pad-medium:first-child'


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

    def create_list_of_dictionary_of_deployment_info(self):
        """
        list of dictionary for deployment info.
        :return: list{'status': 'SUCCESS', 'last_scanned': 'September 26, 2016', 'template': 'Oracle'}
        """
        deployment_info_list = self.locate_element_by_css_selector(DEPLOYMENT_INFO_SELECTOR)
        list_item = {}
        list_item['status'] = deployment_info_list.find_element_by_css_selector(
            "div:nth-child(1) > div:last-child > h4").text
        list_item['template'] = deployment_info_list.find_element_by_css_selector(
            "div:nth-child(2) > div:last-child > h4").text
        list_item['last_scanned'] = deployment_info_list.find_element_by_css_selector(
            "div:nth-child(3) > div:last-child > h4").text
        return list_item
