import unittest

from pages.MenuNavigationPage import MenuNavigationPage
from pages.deployments.DeploymentsPage import DeploymentsPage
from pages.templates.TemplatesMenuListPage import TemplatesMenuListPage
from pages.templates.details.TemplateDetailsPage import TemplateDetailsPage
from tools.ApiUtils import ApiUtils
from tools.DriverUtils import DriverUtils
from tools.ListUtils import ListUtils
from tools.SoftAssert import SoftAssert


class ViewDeploymentComplianceStatusOverviewTest(unittest.TestCase):
    """
    Test will make 3 verification steps:
    In the first one test will navigate to deployments page and grab in a dictionary list all policies displayed with
    their attributes (number of variances, number of times that specific policy types appear) and compare this list
    with a list of dictionary grabbed from API call in setUp method.
    The second step verify that the resources dictionary list [{resource name, status},...] grabbed from application
    interface is the same as the list obtained from API call in setUp method. The status for resource (Warning,
    Compliant,Non Compliant, Unknown) is calculated separated considering complianceScore grabbed from API call.
    The third step verify that the bars dimensions of the policies compliance status overview are the same as those
    that are calculated using compliant scores dates from api calls.
    """

    def setUp(self):
        # self.policies_list = ApiUtils().grab_templates_json()
        # api_policy_types_list = ListUtils().grab_list_of_policies_types(self.policies_list)
        # no_duplicate_policy_type_list = ListUtils().remove_duplicates_from_list(api_policy_types_list)
        # policies_model_list = ListUtils().create_list_of_policies_model(self.policies_list,
        #                                                                 no_duplicate_policy_type_list)


        # self.api_policies_list = ListUtils().sort_list_alphabetically_by('type', policies_model_list)
        # self.api_resource_list_with_status = ListUtils().sort_list_alphabetically_by('name',
        #                                                                              ListUtils().grab_list_of_resources_with_status(
        #                                                                                  self.policies_list))
        # aplication_bar_dimension = 192
        # self.api_policies_dimensions_bar_list = ListUtils().create_list_of_policies_bar_dimensions(
        #     no_duplicate_policy_type_list, self.policies_list, aplication_bar_dimension)


        self.templtes_json = ApiUtils().grab_templates_json()
        self.list_of_templates = ListUtils().grab_template_names_and_id(self.templtes_json)
        random_template_list = ListUtils().return_random_from_list(self.list_of_templates)
        self.random_templateID = random_template_list.get('templateID')
        self.random_templateName = random_template_list.get('templateName')

        self.deployment_list = ListUtils().grab_deployment_name_and_id(self.random_templateID, self.templtes_json)
        random_deployment_list = ListUtils().return_random_from_list(self.deployment_list)
        self.random_deploymentName = random_deployment_list.get('deploymentName')
        self.random_deploymentID = random_deployment_list.get('deploymentId')
        self.api_deployment_info = ListUtils().grab_list_of_deployment_info(self.random_deploymentID,
                                                                            self.templtes_json)
        print "random_deploymentName: ", self.random_deploymentName

        api_policy_types_list = ListUtils().grab_list_of_policies_types('6170',self.templtes_json)
        print "api_policy_types_list: ",api_policy_types_list

        no_duplicate_policy_type_list = ListUtils().remove_duplicates_from_list(api_policy_types_list)
        policies_model_list = ListUtils().create_list_of_policies_model(self.templtes_json,
                                                                        no_duplicate_policy_type_list)

        print "policies_model_list: ",policies_model_list


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
        aplication_policies_list = ListUtils().sort_list_alphabetically_by('type',
                                                                           deployment_page.create_list_of_dictionary_for_policies())

        SoftAssert().verfy_equals_true("List of policies doesn't matched ",
                                       self.api_policies_list, aplication_policies_list)

        aplication_resources_list_with_status = ListUtils().sort_list_alphabetically_by('name',
                                                                                        deployment_page.create_list_of_dictionary_for_resources())

        SoftAssert().verfy_equals_true("List of resources doesn't matched ",
                                       self.api_resource_list_with_status, aplication_resources_list_with_status)

        aplication_policies_dimensions_bar_list = deployment_page.create_list_of_policies_dimensions_bar()

        SoftAssert().verfy_equals_true("List of dimension bar doesn't matched ",
                                       self.api_policies_dimensions_bar_list, aplication_policies_dimensions_bar_list)

        self.assertEqual(SoftAssert().failures_size(), 0, str(SoftAssert().failures_list()))

    def tearDown(self):
        menuNavigationPage = MenuNavigationPage(self.browser)
        menuNavigationPage.close_driver()
