from tools.WebdriverBase import WebdriverBase
import time

RESOURCES_LIST_SELECTOR = 'li[role="listitem"]:not(.grommetux-box--pad-between-small)'
POLICIES_LIST_SELECTOR = 'div.grommetux-box--pad-small div.grommetux-box--pad-medium:nth-child(2) div.grommetux-box--direction-row:not(.grommetux-box--justify-between)'
DEPLOYMENT_INFO_SELECTOR = 'div.grommetux-background-color-index-light-1 div.grommetux-box--pad-medium:first-child'
POLICIES_BAR_LIST_SELECTOR = 'div[class="grommetux-box grommetux-box--direction-row grommetux-box--responsive grommetux-box--pad-none"]'
NOTIFICATION_CONTAINER_SELECTOR = 'section.grommetux-section'


class DeploymentsPage(WebdriverBase):
    """
    Mapping for Deployments Tab
    """

    def __init__(self, driver):
        self.driver = driver

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
        list_item['compliant'] = deployment_info_list.find_element_by_css_selector(
            "div:nth-child(4) > div:last-child > h4").text
        return list_item

    def create_list_of_policies_dimensions_bar(self):
        """
        For every policies types that is displayed creates a list of bar dimensions
        :return: [{'blue': 57, 'gray': 36, 'type': u'Policy type', 'red': 72, 'yellow': 29},{...}]
        """
        policies_bar_list = self.locate_elements_by_css_selector(POLICIES_BAR_LIST_SELECTOR)
        return_list = []
        for item in policies_bar_list:
            list_item = {}
            list_item['type'] = item.find_element_by_css_selector('label').text
            path_list = item.find_elements_by_css_selector("g.grommetux-meter__values g path.grommetux-meter__slice")
            for path in path_list:
                class_atribute = path.get_attribute("class")
                if "accent" in class_atribute:
                    value = path.get_attribute("d")
                    list_item['blue'] = self.return_bar_dimension(value)
                if "warning" in class_atribute:
                    value = path.get_attribute("d")
                    list_item['yellow'] = self.return_bar_dimension(value)
                if "critical" in class_atribute:
                    value = path.get_attribute("d")
                    list_item['red'] = self.return_bar_dimension(value)
                if "unset" in class_atribute:
                    value = path.get_attribute("d")
                    list_item['gray'] = self.return_bar_dimension(value)
            return_list.append(list_item)
        return return_list

    def return_bar_dimension(self, value):
        """
        Return bar dimension by calculating it from html 'd' attribute value of each bar.
        :param value:
        :return: dimension
        """
        split_value = value.split(" ")
        first_value_splited = split_value[0].split("M")
        first_value = first_value_splited[1]
        second_value_splited = split_value[1].split("L")
        second_value = second_value_splited[1]
        dimension = int(float(second_value.replace(',', '.')) - float(first_value.replace(',', '.')))
        return dimension

    def get_notification_message(self):
        """
        When is displayed, grab notification message
        :return:
        """
        message = self.locate_element_by_css_selector('span.grommetux-notification__message').text
        return message

    def get_notification_date(self):
        """
        When is displayed, grab notification message
        :return:
        """
        message = self.locate_element_by_css_selector(
            'div.grommetux-box--pad-horizontal-small span:first-child span:first-child').text
        date = self.locate_element_by_css_selector(
            'div.grommetux-box--pad-horizontal-small span:first-child span:last-child').text
        complete_message = message + ' ' + date
        return complete_message

    def get_container_number(self):
        """
        Return the number of containers that are displayed to verify if notification message container is displayed
        :return:
        """
        container_list = self.locate_elements_by_css_selector(
            '.grommetux-box--pad-vertical-small.grommetux-background-color-index-light-2 > *')
        return len(container_list)

    def wait_until_notification_disappear(self):
        """
        Wait until notification message container disappear
        :return:
        """
        i = 0
        while self.get_container_number() != 1 or i < 20:
            time.sleep(1)
            i += 1
