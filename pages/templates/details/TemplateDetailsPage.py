from tools.WebdriverBase import WebdriverBase
import time

GROUP_CONTAINERS = '.grommetux-box--pad-small'
DEPLOYMENT_LIST = 'div.grommetux-box--pad-small:last-child ul ul li'

RESOURCE_TYPES_LIST_SELECTOR = 'div.grommetux-box--pad-small:nth-child(1) li.grommetux-box--pad-medium'
POLICIES_LIST_SELECTOR = 'div.grommetux-box--pad-small:nth-child(2) li.grommetux-box--pad-medium'
DEPLOYMENTS_LIST_SELECTOR = 'div.grommetux-box--pad-small:nth-child(3) li.grommetux-box--pad-medium'


class TemplateDetailsPage(WebdriverBase):
    """
    Details related to template. Page contains Resources, Policies, Deployments and actions(deploy, schedule) on current template
    """

    def grab_resource_types_list(self):
        resource_types = []
        resource_type_list = self.locate_elements_by_css_selector(RESOURCE_TYPES_LIST_SELECTOR)
        for resource_now in resource_type_list:
            resource_types.append(resource_now.text)
        return resource_types

    def grab_policies_list(self):
        policies = []
        policies_list = self.locate_elements_by_css_selector(POLICIES_LIST_SELECTOR)
        for policies_now in policies_list:
            policies.append(policies_now.text)
        return policies

    def grab_deployments_dictionary_list(self):
        deployments_list = []
        policies_list = self.locate_elements_by_css_selector(DEPLOYMENT_LIST)
        for deployment_now in policies_list:
            deployments={}
            deployments['name']=deployment_now.find_element_by_css_selector('div:first-child label').text
            deployments['status']=deployment_now.find_element_by_css_selector('div:last-child').text
            deployments_list.append(deployments)
        return deployments_list

    def select_deployment_by_name(self, deployment_name):
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
