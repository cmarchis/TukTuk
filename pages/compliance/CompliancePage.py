from tools.WebdriverBase import WebdriverBase
import time
from selenium.webdriver.support.ui import Select

POLICY_CONTAINER_SELECTOR = "div.index-tiles__section"
FILTER_SELETOR = "button.index-filters__menu"
STATUS_SELECTOR = "div.index-filter__body label span.grommetux-check-box__label span"
SORT_SELECTOR = "div > select"
SORT_ICON_SELECTOR = "div.grommetux-menu__drop--align-right span>svg.grommetux-control-icon-filter"


class CompliancePage(WebdriverBase):
    def __init__(self, driver):
        self.driver = driver

    def create_list_of_dictionary_for_compliance(self):
        policy_list = self.locate_elements_by_css_selector(POLICY_CONTAINER_SELECTOR)
        return_list = []
        for item_now in policy_list:
            list_item = {}
            policy_name_list = item_now.find_elements_by_css_selector("div div.grommetux-tile--hover-border-small")
            for item_now2 in policy_name_list:
                list_item = {}
                list_item['key'] = item_now.find_element_by_css_selector("header label").text
                list_item['name'] = item_now2.find_element_by_css_selector("label.grommetux-label--medium strong").text
                abc = item_now2.find_element_by_css_selector("label.grommetux-label--medium strong").text
                list_item['status'] = (item_now2.find_element_by_css_selector("label:last-child").text).upper()
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

    def select_status(self, status):
        filter_button = self.locate_element_by_css_selector(FILTER_SELETOR)
        filter_button.click()
        status_option_list = self.locate_elements_by_css_selector(STATUS_SELECTOR)
        for item in status_option_list:
            if item.text == status:
                item.click()
                time.sleep(2)
                break
        filter_button_open = self.locate_element_by_css_selector(SORT_ICON_SELECTOR)
        filter_button_open.click()

    def select_sort_option(self, sort_option):
        filter_button = self.locate_element_by_css_selector(FILTER_SELETOR)
        filter_button.click()
        sort_drop_down = Select(self.locate_element_by_css_selector(SORT_SELECTOR))
        sort_drop_down.select_by_visible_text(sort_option)
        time.sleep(2)
        filter_button_open = self.locate_element_by_css_selector(SORT_ICON_SELECTOR)
        filter_button_open.click()

    def scroll_until_all_policies_types_are_visible(self, api_list_compliance):
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
        while len(
                self.create_list_of_dictionary_for_compliance()) != api_list_compliance and i < 5:
            self.scroll_pg_down()
            i += 1

    def click_compliance(self, compliance_id):
        compliance_container = self.locate_elements_by_css_selector(POLICY_CONTAINER_SELECTOR)
        for compliance_now in compliance_container:
            compliance_list = compliance_now.find_elements_by_css_selector('div div')
            for item_now in compliance_list:
                if item_now.get_attribute('aria-label') == compliance_id:
                    item_now.click()
                    break
