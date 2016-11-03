from tools.WebdriverBase import WebdriverBase
import time

GROUP_CONTAINERS = '.grommetux-box--pad-small'
DEPLOYMENT_LIST = 'div.grommetux-box--pad-small:last-child ul ul li'


class TemplateDetailsPage(WebdriverBase):
    """
    Details related to template. Page contains Resources, Policies, Deployments and actions(deploy, schedule) on current template
    """

    def grab_resources_data(self):
        return self.grab_generic_data(0)

    def grab_policies_data(self):
        return self.grab_generic_data(1)

    def grab_deployments_data(self):
        return self.grab_generic_data(2)

    def grab_generic_data(self, container_number):
        result_list = []
        all_containers = self.locate_elements_by_css_selector(GROUP_CONTAINERS)
        if len(all_containers) == 3:
            data_rows = all_containers[container_number].find_elements_by_css_selector('[role="listitem"]')
            for data_now in data_rows:
                result_list.append(data_now.text)

        result_list.pop(0)
        return result_list

    def select_deployment(self, deployment_name):
        deployments_list = self.locate_elements_by_css_selector(DEPLOYMENT_LIST)
        for deployment in deployments_list:
            list_deployment_name = deployment.find_element_by_css_selector('div:first-child').text
            if list_deployment_name == deployment_name:
                deployment.click()
                break

    def select_deployment_by_id(self, deployment_id):
        deployments_list = self.locate_elements_by_css_selector(DEPLOYMENT_LIST)
        for deployment in deployments_list:
            if deployment.get_attribute("id") == deployment_id:
                deployment.click()
                time.sleep(2)
                break
