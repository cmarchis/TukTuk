from tools.WebdriverBase import WebdriverBase
import time
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys

COMPLIANCE_CONTAINERS_SECTIONS_SELECTOR = "section.grommetux-section"
COMPLIANCE_CONTAINER_SELECTOR = "section.grommetux-section"
FILTER_SELECTOR = "svg.grommetux-control-icon-filter"
STATUS_LIST_SELECTOR = "ol.grommetux-select__options li label"
SORT_DROP_DOWN_BUTTON_SELECTOR = "svg.grommetux-control-icon-caret-down"
CLOSE_FILTER_ICON_SELECTOR = "div.grommetux-sidebar--large svg.grommetux-control-icon-close"
SORT_OPTION_LIST = "div.grommetux-select__drop ol.grommetux-select__options li"
SORT_ASCENDING = "svg.grommetux-control-icon-link-down"
SORT_DESCENDING = "svg.grommetux-control-icon-link-up"
COMPLIANCE_LABEL_LIST_SELECTOR = 'label.grommetux-label--medium strong'


class CompliancePage(WebdriverBase):
    def __init__(self, driver):
        self.driver = driver

    def create_list_of_dictionary_for_compliance(self):
        section_list = self.locate_elements_by_css_selector(COMPLIANCE_CONTAINERS_SECTIONS_SELECTOR)
        return_list = []
        for section in section_list:
            compliance_list = section.find_elements_by_css_selector("div[id]")
            for item_now in compliance_list:
                list_item = {}
                list_item['key'] = section.find_element_by_css_selector("header label").text
                list_item['name'] = item_now.find_element_by_css_selector("label.grommetux-label--medium strong").text
                list_item['status'] = item_now.find_element_by_css_selector("label:last-child").text
                return_list.append(list_item)
        return return_list

    def create_list_of_dictionary_for_compliance_with_id(self):
        section_list = self.locate_elements_by_css_selector(COMPLIANCE_CONTAINERS_SECTIONS_SELECTOR)
        return_list = []
        for section in section_list:
            compliance_list = section.find_elements_by_css_selector("div[id]")
            for item_now in compliance_list:
                list_item = {}
                list_item['key'] = section.find_element_by_css_selector("header label").text
                list_item['name'] = item_now.find_element_by_css_selector("label.grommetux-label--medium strong").text
                list_item['status'] = item_now.find_element_by_css_selector("label:last-child").text
                list_item['id'] = item_now.get_attribute('id')
                return_list.append(list_item)
        return return_list

    def create_list_of_key_dictionary_for_compliance(self):
        section_list = self.locate_elements_by_css_selector(COMPLIANCE_CONTAINERS_SECTIONS_SELECTOR)
        return_list = []
        for section in section_list:
            compliance_list = section.find_elements_by_css_selector("div[id]")
            for item_now in compliance_list:
                list_item = {}
                list_item['key'] = section.find_element_by_css_selector("header label").text
                list_item['name'] = item_now.find_element_by_css_selector("label.grommetux-label--medium strong").text
                list_item['status'] = item_now.find_element_by_css_selector("label:last-child").text
                list_item['id'] = item_now.get_attribute('id')
                return_list.append(list_item)
        return return_list

    def grab_number_of_compliance(self):
        compliance_list = self.locate_elements_by_css_selector(COMPLIANCE_LABEL_LIST_SELECTOR)
        return len(compliance_list)

    def select_sorting_option(self, sorting_key, sorting_type):
        filter_button = self.locate_element_by_css_selector(FILTER_SELECTOR)
        filter_button.click()
        sort_option = Select(self.locate_element_by_css_selector("select.flex"))
        sort_option.select_by_visible_text(sorting_key)
        if sorting_type is "Descending":
            option_descending = self.locate_element_by_css_selector("svg.grommetux-control-icon-link-down")
            option_descending.click()
        else:
            option_ascending = self.locate_element_by_css_selector("svg.grommetux-control-icon-link-up")
            option_ascending.click()
        time.sleep(5)

    def select_status(self, status):
        filter_button = self.locate_element_by_css_selector(FILTER_SELECTOR)
        filter_button.click()
        status_option_list = self.locate_elements_by_css_selector(STATUS_LIST_SELECTOR)
        for item in status_option_list:
            if item.text == status:
                item.click()
                time.sleep(2)
                break
        filter_button_open = self.locate_element_by_css_selector(CLOSE_FILTER_ICON_SELECTOR)
        filter_button_open.click()

    def select_sort_option(self, sort_option):
        filter_button = self.locate_element_by_css_selector(FILTER_SELECTOR)
        filter_button.click()
        sort_drop_down_button = self.locate_element_by_css_selector(SORT_DROP_DOWN_BUTTON_SELECTOR)
        sort_drop_down_button.click()
        sort_option_list = self.locate_elements_by_css_selector(SORT_OPTION_LIST)
        for item in sort_option_list:
            if item.text == sort_option:
                item.click()
                time.sleep(2)
                break
        filter_button_open = self.locate_element_by_css_selector(CLOSE_FILTER_ICON_SELECTOR)
        filter_button_open.click()

    def select_sort_order(self, sort_order):
        filter_button = self.locate_element_by_css_selector(FILTER_SELECTOR)
        filter_button.click()
        if sort_order == "ascending":
            sort_button = self.locate_element_by_css_selector(SORT_ASCENDING)
            sort_button.click()
        elif sort_order == "descending":
            sort_button = self.locate_element_by_css_selector(SORT_DESCENDING)
            sort_button.click()
        filter_button_open = self.locate_element_by_css_selector(CLOSE_FILTER_ICON_SELECTOR)
        filter_button_open.click()

    def scroll_pg_down(self):
        """
        Scroll in webpage by simulating user action of pressing end button
        :return:
        """
        time.sleep(3)
        scroll = self.locate_element_by_css_selector("div.grommetux-tiles div:first-child")
        scroll.send_keys(Keys.END)
        time.sleep(3)

    def scroll_until_all_compliance_are_visible(self, number_of_compliance_from_api):
        """
        Scroll until the length of policies types list grabbed from application is the same as the length of list of
         policies types grabbed from API and if this condition isn't reached will scroll until the number of scroll
         will pe lower than the length of the list containing all the policies grabbed from API dived by the number of
         policies that can be displayed on a view - 5
        :param api_list_policies_types_length: the length of policies types list grabbed from API
        :param api_list_all_policies_length: the length of all policies list grabbed from API
        :return:
        """
        i = 0
        while (self.grab_number_of_compliance() != number_of_compliance_from_api) and (i < 20):
            self.scroll_pg_down()
            time.sleep(5)
            self.scroll_pg_down()
            i += 1

    def scroll_to_home(self):
        self.scroll_to_home()

    def select_compliance_by_id(self, deployment_id, compliance_list_lenght):
        found = False
        compliance_list = self.locate_elements_by_css_selector('div.grommetux-tiles div')
        while found != True and len(compliance_list) < compliance_list_lenght:
            self.scroll_pg_down()
            compliance_list = self.locate_elements_by_css_selector('div.grommetux-tiles div')
            for compliance in compliance_list:
                id = compliance.get_attribute('id')
                if id == deployment_id:
                    compliance.click()
                    time.sleep(3)
                    found = True
                    break
