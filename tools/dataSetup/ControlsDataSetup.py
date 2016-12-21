from tools.ConfigUtils import ConfigUtils
from tools.api.mock.MockControlsApiUtils import MockControlsApiUtils
from tools.api.real.RealApiUtils import RealApiUtils
from tools.utilsList.ControlsListUtils import ControlsListUtils
from tools.ListUtils import ListUtils


class ControlsDataSetup(object):
    api_url = ConfigUtils().read_config_file()['apiBaseURL']
    api_type = ConfigUtils().read_config_file()['apiType']

    def grab_compliance_json(self):
        compliance_json = ''
        if self.api_type == 'real':
            compliance_json = RealApiUtils().grab_controls_json(self.api_url)
        elif self.api_type == 'mock':
            compliance_json = MockControlsApiUtils().grab_controls_json(self.api_url)
        return compliance_json

    def grab_controls_list(self):
        controls_json = self.grab_compliance_json()
        controls_list = ControlsListUtils().grab_controls_dictionary_list(controls_json)
        return controls_list

    def grab_controls_name_list_ascending_order(self):
        controls_json = self.grab_compliance_json()
        controls_name_list = ControlsListUtils().grab_controls_name_list(controls_json)
        ascending_controls_name_list = ListUtils().sort_dictionary_list_alphabetically_ascending_by('name',
                                                                                                    controls_name_list)
        return ascending_controls_name_list

    def grab_controls_name_list_descending_order(self):
        controls_json = self.grab_compliance_json()
        controls_name_list = ControlsListUtils().grab_controls_name_list(controls_json)
        ascending_controls_name_list = ListUtils().sort_dictionary_list_alphabetically_descending_by('name',
                                                                                                     controls_name_list)
        return ascending_controls_name_list
