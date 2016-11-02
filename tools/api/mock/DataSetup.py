from tools.ListUtils import ListUtils
from tools.api.mock.MockApiUtils import MockApiUtils
from tools.ConfigUtils import ConfigUtils




class DataSetup(object):

    def grab_template_data(self):
        self.api_url = ConfigUtils().read_config_file()['apiBaseURL']
        return MockApiUtils().grab_templates_json(self.api_url)

    def get_random_template_id(self):
        list_of_templates = ListUtils().grab_template_names_and_id(self.grab_template_data())
        random_template_list = ListUtils().return_random_from_list(list_of_templates)
        return random_template_list.get('templateID')

    def grab_deployment_data_random(self):
        self.api_url = ConfigUtils().read_config_file()['apiBaseURL']
        return MockApiUtils().grab_deployments_from_templates_json(self.api_url, self.get_random_template_id())

    def grab_deployment_data_by_template_id(self, template_id):
        self.api_url = ConfigUtils().read_config_file()['apiBaseURL']
        return MockApiUtils().grab_deployments_from_templates_json(self.api_url, template_id)

    def grab_random_deployment_id(self):
        random_deployment_list = ListUtils().return_random_from_list(self.grab_deployment_data_random())
        return random_deployment_list.get('deploymentId')


    def grab_resource_data(self):
        self.api_url = ConfigUtils().read_config_file()['apiBaseURL']
        deployment_json_resources = MockApiUtils().grab_deployments_json(self.api_url, self.get_random_template_id())
        return  ListUtils().grab_resources_from_deployment_mock(deployment_json_resources)


    def grab_resource_data_by_template_id(self, template_id):
        self.api_url = ConfigUtils().read_config_file()['apiBaseURL']
        deployment_json_resources = MockApiUtils().grab_deployments_json(self.api_url, template_id)
        return  ListUtils().grab_resources_from_deployment_mock(deployment_json_resources)

    def grab_random_resource_id(self):
        random_resource_list = ListUtils().return_random_from_list(self.grab_resource_data())
        return  random_resource_list.get('resourceId')



if __name__ == "__main__":
    print DataSetup().get_random_template_id()
    print DataSetup().grab_random_resource_id()
    print DataSetup().grab_random_deployment_id()

    print DataSetup().grab_resource_data_by_template_id("4936")
    print DataSetup().grab_deployment_data_by_template_id("4936")