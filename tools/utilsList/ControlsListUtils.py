from tools.ListUtils import ListUtils


class ControlsListUtils(object):
    def grab_controls_dictionary_list(self, controls_json):
        controls_list = []
        for control in controls_json['members']:
            controls_data = {}
            str_key = str(control['modifiedDT'])[0:10]
            long_key = long(str_key)
            controls_data['key'] = ListUtils().convert_timpestamp_to_compliance_sort_time(long_key)
            controls_data['name'] = control['name']
            description = control['description']
            controls_data['description'] = description[0:35] + '...'
            controls_data['id'] = control['id']
            controls_list.append(controls_data)
        return controls_list

    def grab_controls_name_list(self, controls_json):
        controls_list = []
        for control in controls_json['members']:
            controls_data = {}
            controls_data['name'] = control['name']
            controls_list.append(controls_data)
        return controls_list
