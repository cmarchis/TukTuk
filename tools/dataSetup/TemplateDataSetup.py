from tools.utilsList.TemplateListUtils import TemplateListUtils
from tools.ListUtils import ListUtils
from tools.api.mock.MockTemplateApiUtils import MockTemplateApiUtils
from tools.api.real.RealApiUtils import RealApiUtils
from tools.ConfigUtils import ConfigUtils


class TemplateDataSetup(object):
    api_url = ConfigUtils().read_config_file()['apiBaseURL']
    api_type = ConfigUtils().read_config_file()['apiType']

    def grab_template_data(self):
        template_data = ''
        if self.api_type == 'real':
            template_data = RealApiUtils().grab_templates_json(self.api_url)
        elif self.api_type == 'mock':
            template_data = MockTemplateApiUtils().grab_templates_json(self.api_url)
        return template_data

    def get_random_template_id(self):
        list_of_templates = TemplateListUtils().grab_template_names_and_id(self.grab_template_data())
        random_template_list = ListUtils().return_random_from_list(list_of_templates)
        return random_template_list.get('templateID')

    def grab_random_deployment_id_by_template_id(self, template_id):
        template_json = self.grab_template_data()
        deployments_list = TemplateListUtils().grab_deployment_list_from_template_json_by_template_id(template_json,
                                                                                                      template_id)
        random_deployment = ListUtils().return_random_from_list(deployments_list)
        random_deployment_id = random_deployment.get('deploymentId')
        return random_deployment_id

    def grab_template_dictionary_list(self):
        template_json = self.grab_template_data()
        template_dictionary_list = TemplateListUtils().grab_template_dictionary_list(template_json)
        return ListUtils().sort_dictionary_list_alphabetically_ascending_by('name', template_dictionary_list)

    def grab_resources_types_for_template_id(self, template_id):
        template_json = self.grab_template_data()
        return TemplateListUtils().grab_template_resources_types_for_template_id(template_id, template_json)

    def grab_template_policies_for_template_id(self, template_id):
        template_json = self.grab_template_data()
        return TemplateListUtils().grab_template_policies_for_template_id(template_id, template_json)

    def grab_deployments_dictionary_list_for_template_id(self, template_id):
        template_json = self.grab_template_data()
        deployments_dictionary_list = TemplateListUtils().grab_deployment_list_from_template_json_by_template_id(
            template_json, template_id)
        return deployments_dictionary_list
