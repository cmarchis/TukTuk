from tools.api.mock.MockComplianceApiUtils import MockComplianceApiUtils
from tools.utilsList.ComplianceListUtils import ComplianceListUtils
from tools.ConfigUtils import ConfigUtils
from tools.api.real.RealApiUtils import RealApiUtils
from tools.ListUtils import ListUtils


class ComplianceDataSetup(object):
    api_url = ConfigUtils().read_config_file()['apiBaseURL']
    api_type = ConfigUtils().read_config_file()['apiType']

    def grab_compliance_json(self):
        compliance_json = ''
        if self.api_type == 'real':
            compliance_json = RealApiUtils().grab_compliance_json(self.api_url)
        elif self.api_type == 'mock':
            compliance_json = MockComplianceApiUtils().grab_compliance_json(self.api_url)
        return compliance_json

    def grab_sorted_ascending_compliance_json(self):
        compliance_json = ''
        if self.api_type == 'real':
            compliance_json = RealApiUtils().grab_sorted_compliance_json(self.api_url)
        elif self.api_type == 'mock':
            compliance_json = MockComplianceApiUtils().grab_sorted_ascending_compliance_json(self.api_url)
        return compliance_json

    def grab_sorted_descending_compliance_json(self):
        compliance_json = ''
        if self.api_type == 'real':
            compliance_json = RealApiUtils().grab_sorted_compliance_json(self.api_url)
        elif self.api_type == 'mock':
            compliance_json = MockComplianceApiUtils().grab_sorted_descending_compliance_json(self.api_url)
        return compliance_json

    def grab_all_compliance_list(self):
        compliance_json = self.grab_compliance_json()
        compliance_list = ComplianceListUtils().grab_compliance_resources(compliance_json)
        return compliance_list

    def grab_compliance_list_of_given_status(self, key):
        compliance_list = self.grab_all_compliance_list()
        list_of_given_status = ComplianceListUtils().create_compliance_list(key, compliance_list)
        return list_of_given_status

    def grab_compliance_list_sorted_by_key(self, sort_option):
        compliance_json = self.grab_compliance_json()
        compliance_list = ComplianceListUtils().grab_compliance_resources_key_sorted_by_key(sort_option,
                                                                                            compliance_json)
        return compliance_list

    def grab_random_compliance_id(self):
        compliance_json = self.grab_compliance_json()
        compliance_id_list = ComplianceListUtils().grab_compliance_id_list(compliance_json)
        random_compliance = ListUtils().return_random_from_list(compliance_id_list)
        return random_compliance

    def grab_number_of_compliance(self):
        compliance_json = self.grab_compliance_json()
        compliance_id_list = ComplianceListUtils().grab_compliance_id_list(compliance_json)
        return len(compliance_id_list)

    def grab_compliance_details(self, compliance_id):
        compliance_json = self.grab_compliance_json()
        compliance_details_dictionary_list = ComplianceListUtils().grab_compliance_details_list(compliance_json,
                                                                                                compliance_id)
        return compliance_details_dictionary_list

    def grab_sorted_ascending_compliance_list(self, key_name):
        sorted_compliance_json = self.grab_sorted_ascending_compliance_json()
        compliance_list = ComplianceListUtils().grab_compliance_resources_key_sorted_by_key_with_id(key_name,
                                                                                            sorted_compliance_json)
        return compliance_list

    def grab_sorted_descending_compliance_list(self, key_name):
        sorted_compliance_json = self.grab_sorted_descending_compliance_json()
        compliance_list = ComplianceListUtils().grab_compliance_resources_key_sorted_by_key_with_id(key_name,
                                                                                            sorted_compliance_json)
        return compliance_list
