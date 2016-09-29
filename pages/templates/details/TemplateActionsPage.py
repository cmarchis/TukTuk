from tools.WebdriverBase import WebdriverBase


ACTIONS_CONTAINERS = '.grommetux-box--separator-all.grommetux-box--pad-horizontal-medium'

class TemplatActionsPage(WebdriverBase):

    def grab_actions_label(self):
        actions_container = self.locate_element_by_css_selector(ACTIONS_CONTAINERS)
        label_element = actions_container.find_element_by_css_selector('div:first-child')
        return label_element.text

    def click_deploy(self):
        actions_container = self.locate_element_by_css_selector(ACTIONS_CONTAINERS)
        actions_element = actions_container.find_element_by_css_selector('div:last-child button:first-child')
        actions_element.click()

    def click_schedule(self):
        actions_container = self.locate_element_by_css_selector(ACTIONS_CONTAINERS)
        actions_element = actions_container.find_element_by_css_selector('div:last-child button:last-child')
        actions_element.click()