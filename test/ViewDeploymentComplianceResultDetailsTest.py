import unittest
from operator import itemgetter

from pages.MenuNavigationPage import MenuNavigationPage
from pages.compliance.CompliancePage import CompliancePage
from pages.deployments.DeploymentsPage import DeploymentsPage
from pages.templates.TemplatesMenuListPage import TemplatesMenuListPage
from pages.templates.details.TemplateDetailsPage import TemplateDetailsPage
from tools.DriverUtils import DriverUtils
from tools.ListUtils import ListUtils
from tools.SoftAssert import SoftAssert
from tools.api.mock.MockApiUtils import ApiUtils


class ViewDeploymentComplianceResultDetailsTest(unittest.TestCase):
    def setUp(self):
        # get Template
        templates_json = ApiUtils().grab_templates_json()
        list_of_templates = ListUtils().grab_template_names_and_id(templates_json)
        random_template_list = ListUtils().return_random_from_list(list_of_templates)
        random_templateID = random_template_list.get('templateID')
        self.random_templateName = random_template_list.get('templateName')

        # get Deployment
        deployment_list = ListUtils().grab_deployment_name_and_id(random_templateID, templates_json)
        random_deployment_list = ListUtils().return_random_from_list(deployment_list)
        self.random_deploymentName = random_deployment_list.get('deploymentName')
        random_deploymentID = random_deployment_list.get('deploymentId')

        # get Resources
        resource_list = ListUtils().grab_resources_from_deployment(random_deploymentID, templates_json)
        random_resource_list = ListUtils().return_random_from_list(resource_list)
        self.random_resource_id = random_resource_list.get('resourceId')

        # get Compliance
        compliance_json = ApiUtils().grab_compliance_json_for_resource_id(self.random_resource_id)
        self.api_compliance_list_dictionary = ListUtils().grab_compliance_resources(compliance_json)
        self.api_sorted_compliance_dictionary = sorted(self.api_compliance_list_dictionary,
                                                       key=itemgetter('name', 'key', 'status'))
        self.api_compliance_filtered_by_status = ListUtils().create_compliance_list('COMPLIANT',
                                                                                    self.api_sorted_compliance_dictionary)
        self.api_sorted_compliance_list_dictionary = sorted(self.api_compliance_filtered_by_status,
                                                            key=itemgetter('name', 'key', 'status'))

        self.api_compliance_list_dictionary_sorted_by_key = ListUtils().grab_compliance_resources_key("Requirement",
                                                                                                      compliance_json)
        self.api_compliance_list_dictionary_sort = ListUtils().sort_list_dictionary_natural_ascending(
            self.api_compliance_list_dictionary_sorted_by_key)

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
        compliance_page.scroll_until_all_policies_types_are_visible(len(self.api_compliance_list_dictionary))
        aplication_compliance_list = compliance_page.create_list_of_dictionary_for_compliance()

        aplication_sorted_compliance_dictionary = sorted(aplication_compliance_list,
                                                         key=itemgetter('name', 'key', 'status'))

        SoftAssert().verfy_equals_true(
            "List of compliance grabbed from API doesn't matches with the one grabbed from UI ",
            self.api_sorted_compliance_dictionary,
            aplication_sorted_compliance_dictionary)

        compliance_page.select_status('Compliant')

        compliance_page.scroll_until_all_policies_types_are_visible(len(self.api_compliance_filtered_by_status))
        aplication_compliance_filter_list_dictionary = compliance_page.create_list_of_dictionary_for_compliance()
        aplication_compliance_filter_list_dictionary_sorted = sorted(aplication_compliance_filter_list_dictionary,
                                                                     key=itemgetter('name', 'key', 'status'))

        SoftAssert().verfy_equals_true(
            "List of compliance, filter by status, grabbed from API and doesn't matches with the one grabbed from UI ",
            self.api_sorted_compliance_list_dictionary,
            aplication_compliance_filter_list_dictionary_sorted)

        compliance_page.select_status('All')
        compliance_page.select_sort_option("Requirement")
        aplication_compliance_list_dictionary_sort = compliance_page.create_list_of_dictionary_for_compliance()

        SoftAssert().verfy_equals_true(
            "List of compliance, sorted, grabbed from API and doesn't matches with the one grabbed from UI ",
            self.api_compliance_list_dictionary_sort,
            aplication_compliance_list_dictionary_sort)

        self.assertEqual(SoftAssert().failures_size(), 0, str(SoftAssert().failures_list()))

    def tearDown(self):
        menuNavigationPage = MenuNavigationPage(self.browser)
        menuNavigationPage.close_driver()
