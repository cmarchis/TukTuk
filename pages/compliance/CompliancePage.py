from tools.WebdriverBase import WebdriverBase
import time
from selenium.webdriver.support.ui import Select

POLICY_CONTAINER_SELECTOR = "div.index-tiles__section"
FILTER_SELETOR = "button.index-filters__menu"


class CompliancePage(WebdriverBase):
    def __init__(self, driver):
        self.driver = driver

    def create_list_of_dictionary_for_resources(self):
        policy_list = self.locate_elements_by_css_selector(POLICY_CONTAINER_SELECTOR)
        return_list = []
        for item_now in policy_list:
            list_item = {}
            policy_name_list = item_now.find_elements_by_css_selector("div div.grommetux-tile--hover-border-small")
            for item_now2 in policy_name_list:
                list_item = {}
                list_item['policy_type'] = item_now.find_element_by_css_selector("header label").text
                list_item['name'] = item_now2.find_element_by_css_selector("label.grommetux-label--medium strong").text
                abc = item_now2.find_element_by_css_selector("label.grommetux-label--medium strong").text
                list_item['status'] = item_now2.find_element_by_css_selector("label:last-child").text
                return_list.append(list_item)
        return return_list

    def select_sorting_option(self, sorting_key, sorting_type):
        filter_button = self.locate_element_by_css_selector(FILTER_SELETOR)
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
