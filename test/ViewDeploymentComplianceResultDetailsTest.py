import unittest

from pages.MenuNavigationPage import MenuNavigationPage
from pages.compliance.CompliancePage import CompliancePage
from pages.templates.TemplatesMenuListPage import TemplatesMenuListPage
from pages.templates.details.TemplateDetailsPage import TemplateDetailsPage
from pages.deployments.DeploymentsPage import DeploymentsPage
from tools.SoftAssert import SoftAssert

from tools.DriverUtils import DriverUtils
from tools.ApiUtils import ApiUtils
from tools.ListUtils import ListUtils
from operator import itemgetter


class ViewDeploymentComplianceStatusOverviewTest(unittest.TestCase):
    def setUp(self):
        self.templtes_json = ApiUtils().grab_templates_json()
        self.list_of_templates = ListUtils().grab_template_names_and_id(self.templtes_json)
        random_template_list = ListUtils().return_random_from_list(self.list_of_templates)
        self.random_templateID = random_template_list.get('templateID')
        self.random_templateName = random_template_list.get('templateName')

        self.deployment_list = ListUtils().grab_deployment_name_and_id(self.random_templateID, self.templtes_json)
        random_deployment_list = ListUtils().return_random_from_list(self.deployment_list)
        self.random_deploymentName = random_deployment_list.get('deploymentName')
        self.random_deploymentID = random_deployment_list.get('deploymentId')

        resource_list = ListUtils().grab_resources_from_deployment(self.random_deploymentID, self.templtes_json)
        random_resource_list = ListUtils().return_random_from_list(resource_list)
        self.random_resource_id = random_resource_list.get('resourceId')

        compliance = ApiUtils().grab_resources_json(self.random_resource_id)

        self.compliance_resources_api = ListUtils().grab_compliance_resources(compliance)

        self.browser = DriverUtils().start_driver()

    def test_ViewDeploymentComplianceStatusOverviewTest(self):
        menu_navigation_page = MenuNavigationPage(self.browser)
        menu_navigation_page.navigate_to("http://localhost:8014/provision")
        menu_navigation_page.navigate_to("http://localhost:8014/provision")
        templates_menu_list_page = TemplatesMenuListPage(self.browser)
        templates_menu_list_page.click_on_template_item(self.random_templateName)

        template_details_page = TemplateDetailsPage(self.browser)
        template_details_page.select_deployment(self.random_deploymentName)

        deployment_page = DeploymentsPage(self.browser)
        deployment_page.select_resource_by_id(self.random_resource_id)

        compliance_page = CompliancePage(self.browser)
        compliance_page.scroll_until_all_policies_types_are_visible(len(self.compliance_resources_api))
        compliance_list_aplication = compliance_page.create_list_of_dictionary_for_resources()

        sorted_compliance_resources_api = sorted(self.compliance_resources_api,
                                                 key=itemgetter('name', 'policy_type', 'status'))
        sorted_compliance_list_aplication = sorted(compliance_list_aplication,
                                                   key=itemgetter('name', 'policy_type', 'status'))

        # compliance_resource_sorted_by_status_api = ListUtils().create_compliance_list('COMPLIANT', sorted_compliance_resources_api)

        SoftAssert().verfy_equals_true("List of Results", sorted_compliance_resources_api,
                                       sorted_compliance_list_aplication)

        compliance_resource_sorted_by_status_api = ListUtils().create_compliance_list('COMPLIANT',
                                                                                      sorted_compliance_resources_api)
        compliance_page.select_status('Compliant')

        compliance_page.scroll_until_all_policies_types_are_visible(len(compliance_resource_sorted_by_status_api))
        aplication_compliance_list_status = compliance_page.create_list_of_dictionary_for_resources()
        aplication_sorted_compliance_list_status = sorted(aplication_compliance_list_status,
                                                          key=itemgetter('name', 'policy_type', 'status'))
        api_sorted_compliance_list_status = sorted(compliance_resource_sorted_by_status_api,
                                                   key=itemgetter('name', 'policy_type', 'status'))

        SoftAssert().verfy_equals_true("List of Results sorted", api_sorted_compliance_list_status,
                                       aplication_sorted_compliance_list_status)

        self.assertEqual(SoftAssert().failures_size(), 0, str(SoftAssert().failures_list()))

    def tearDown(self):
        menuNavigationPage = MenuNavigationPage(self.browser)
        menuNavigationPage.close_driver()
