from tools.WebdriverBase import WebdriverBase
from selenium.webdriver.common.keys import Keys
import time


class DeploymentsPage(WebdriverBase):
    def scroll_page_down(self):
        """
        Scroll in webpage by simulating user action of pressing end button
        :return:
        """
        time.sleep(3)
        scroll = self.locate_element_by_css_selector("div.grommetux-tiles a:first-child")
        scroll.send_keys(Keys.END)
        time.sleep(3)

    def select_deployment_by_id(self, deployment_id, deployments_list_lenght):
        found = False
        deployments_list = self.locate_elements_by_css_selector('div.grommetux-tiles a')
        while found != True and len(deployments_list) < deployments_list_lenght:
            self.scroll_page_down()
            deployments_list = self.locate_elements_by_css_selector('div.grommetux-tiles a')
            for deployment in deployments_list:
                id_elem = deployment.find_element_by_css_selector('div[id]')
                id = id_elem.get_attribute('aria-label')
                if id == deployment_id:
                    deployment.click()
                    found = True
                    break
