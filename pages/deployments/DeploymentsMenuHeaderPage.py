from tools.WebdriverBase import WebdriverBase

MENU_HEADER_CONTAINER_LOCATOR = 'div.grommetux-box--justify-end button'


class DeploymentsMenuHeaderPage(WebdriverBase):
    """
    Actions related to Deployments top action bar
    """

    def click_on_header_menu_item(self, name):
        """
        Will select a menu item from the Left side navigation. A label name should be provided.
        :param name:
        :return:
        """
        menu_links_list = self.locate_elements_by_css_selector(MENU_HEADER_CONTAINER_LOCATOR)
        for item_now in menu_links_list:
            if item_now.text == name:
                item_now.click()
                break
