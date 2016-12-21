from tools.WebdriverBase import WebdriverBase
import time
from selenium.webdriver.common.keys import Keys

CONTROLS_LIST_SECTION_SELECTOR = 'div.grommetux-box--pad-none section'
CONTROLS_LIST_SELECTOR = 'div.grommetux-tiles a'
FILTER_SELECTOR = 'svg.grommetux-control-icon-filter'
DROP_DOWN_SELECTOR = 'svg.grommetux-control-icon-caret-down'
FILTER_DROP_DOWN_LIST = 'ol.grommetux-select__options li'
CLOSE_FILTER_SELECTOR = 'div.grommetux-sidebar--large svg.grommetux-control-icon-close'
DESCENDING_ORDER_SELECTOR = 'svg.grommetux-control-icon-link-up'


class ControlsPage(WebdriverBase):
    def __init__(self, driver):
        self.driver = driver

    def scroll_pg_down(self):
        """
        Scroll in webpage by simulating user action of pressing end button
        :return:
        """
        time.sleep(3)
        scroll = self.locate_element_by_css_selector("div.grommetux-tiles a:first-child")
        scroll.send_keys(Keys.END)
        time.sleep(3)

    def grab_number_of_controls(self):
        compliance_list = self.locate_elements_by_css_selector(CONTROLS_LIST_SELECTOR)
        return len(compliance_list)

    def scroll_until_all_controls_are_visible(self, number_of_controls_from_api):
        i = 0
        while (self.grab_number_of_controls() != number_of_controls_from_api) and (i < 20):
            self.scroll_pg_down()
            time.sleep(5)
            self.scroll_pg_down()
            i += 1

    def grab_controls_dictionary_list(self):
        controls_section_list = self.locate_elements_by_css_selector(CONTROLS_LIST_SECTION_SELECTOR)
        controls_data_list = []
        for section in controls_section_list:
            control_list = section.find_elements_by_css_selector("div a")
            for control in control_list:
                control_data = {}
                control_data['key'] = section.find_element_by_css_selector("header label").text
                control_data['name'] = control.find_element_by_css_selector("label strong").text
                control_data['description'] = control.find_element_by_css_selector("label:last-child").text
                control_data['id'] = control.get_attribute('id')
                controls_data_list.append(control_data)
        return controls_data_list

    def grab_name_controls_dictionary_list(self):
        controls_section_list = self.locate_elements_by_css_selector(CONTROLS_LIST_SECTION_SELECTOR)
        controls_data_list = []
        for section in controls_section_list:
            control_list = section.find_elements_by_css_selector("div a")
            for control in control_list:
                control_data = {}
                control_data['name'] = control.find_element_by_css_selector("label strong").text
                controls_data_list.append(control_data)
        return controls_data_list

    def select_sorting_type(self, sorting_option):
        filer_button = self.locate_element_by_css_selector(FILTER_SELECTOR)
        filer_button.click()
        time.sleep(2)
        drop_down_button = self.locate_element_by_css_selector(DROP_DOWN_SELECTOR)
        drop_down_button.click()
        time.sleep(2)
        option_list = self.locate_elements_by_css_selector(FILTER_DROP_DOWN_LIST)
        for option in option_list:
            if option.text == sorting_option:
                option.click()
                break
        close_filter_button = self.locate_element_by_css_selector(CLOSE_FILTER_SELECTOR)
        close_filter_button.click()

    def select_descending_sorting(self):
        time.sleep(2)
        filer_button = self.locate_element_by_css_selector(FILTER_SELECTOR)
        time.sleep(2)
        filer_button.click()
        time.sleep(2)
        descending_button = self.locate_element_by_css_selector(DESCENDING_ORDER_SELECTOR)
        descending_button.click()
        time.sleep(2)
        close_filter_button = self.locate_element_by_css_selector(CLOSE_FILTER_SELECTOR)
        close_filter_button.click()
