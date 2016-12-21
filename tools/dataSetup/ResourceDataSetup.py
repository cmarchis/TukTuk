from tools.utilsList.ResourceListUtils import ResourceListUtils
from tools.ListUtils import ListUtils
from tools.api.mock.MockApiUtils import MockApiUtils
from tools.api.real.RealApiUtils import RealApiUtils
from tools.ConfigUtils import ConfigUtils


class ResourceDataSetup(object):
    api_url = ConfigUtils().read_config_file()['apiBaseURL']
    api_type = ConfigUtils().read_config_file()['apiType']

    def grab_resource_json(self):
        resource_json = ''
        if self.api_type == 'real':
            resource_json = RealApiUtils().grab_resource_json(self.api_url)
        elif self.api_type == 'mock':
            resource_json = MockApiUtils().grab_resource_json(self.api_url)
        return resource_json

    def grab_compliances_for_resources_id(self, resource_id):
        resource_compliance_json = ''
        if self.api_type == 'real':
            resource_compliance_json = RealApiUtils().grab_compliance_for_resource_id(self.api_url)
        elif self.api_type == 'mock':
            resource_compliance_json = MockApiUtils().grab_compliance_for_resource_id(self.api_url, resource_id)
        return resource_compliance_json

    def grab_deployment_compliance_details_for_resource_id(self, resource_id):
        resource_compliance_json = ''
        if self.api_type == 'real':
            resource_compliance_json = RealApiUtils().grab_deployment_compliance_details_for_resource_id(self.api_url)
        elif self.api_type == 'mock':
            resource_compliance_json = MockApiUtils().grab_deployment_compliance_details_for_resource_id(self.api_url,
                                                                                                         resource_id)
        return resource_compliance_json

    def grab_compliance_list_for_resource_id(self, resource_id):
        resource_compliance_json = self.grab_compliances_for_resources_id(resource_id)
        resource_compliance_list = ResourceListUtils().grab_compliance_list_from_resource_id_compliance_json(
            resource_compliance_json)
        return resource_compliance_list

    def grab_random_resouce_id(self):
        resource_json = self.grab_resource_json()
        resource_list = ResourceListUtils().grab_resource_dictionary_list(resource_json)
        random_resource = ListUtils().return_random_from_list(resource_list)
        return random_resource.get('resourceId')

    def grab_random_compliance_id_from_resouce_compliance_list(self, resource_compliance_list):
        random_compliance = ListUtils().return_random_from_list(resource_compliance_list)
        return random_compliance.get('id')

    def grab_resource_compliance_details_data(self, resource_id, compliance_id):
        resource_compliance_json = self.grab_compliances_for_resources_id(resource_id)
        resource_compliance_details = ResourceListUtils().grab_compliance_details_from_resource_id_compliance_json(
            resource_compliance_json, compliance_id)
        return resource_compliance_details

    def grab_deployment_id_for_resource_id(self, resource_id):
        resource_json = self.grab_resource_json()
        deployment_id_by_resource_id = ResourceListUtils().grab_deployment_id_by_resource_id_from_resource_json(
            resource_json, resource_id)
        return deployment_id_by_resource_id

    def grab_resource_info(self, resource_id):
        deployment_id = self.grab_deployment_id_for_resource_id(resource_id)
        deployment_resource_json = self.grab_deployment_compliance_details_for_resource_id(deployment_id)
        compliant = ResourceListUtils().grab_compliance_score_for_resource(deployment_resource_json, resource_id)
        resource_json = self.grab_resource_json()
        resource_info = ResourceListUtils().grab_resource_info_from_resource_json(resource_json, resource_id)
        resource_info.update(compliant)
        return resource_info

    def grab_credential_for_resource_id_json(self, resource_id):
        credential_for_resource_id_json = ''
        if self.api_type == 'real':
            credential_for_resource_id_json = RealApiUtils().grab_credentials_for_resource_id(self.api_url)
        elif self.api_type == 'mock':
            credential_for_resource_id_json = MockApiUtils().grab_credentials_for_resource_id(self.api_url, resource_id)
            return credential_for_resource_id_json

    def grab_credential_list_for_resource_id(self, resource_id):
        credential_resource_json = self.grab_credential_for_resource_id_json(resource_id)
        credential_list = ResourceListUtils().grab_credential_list(credential_resource_json)
        return credential_list


if __name__ == "__main__":
    print "aa: ", ResourceDataSetup().grab_resource_info('8638')
