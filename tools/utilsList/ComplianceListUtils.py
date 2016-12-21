class ComplianceListUtils(object):
    def grab_compliance_resources(self, compliance_json):
        """
        Create a list of dictionary for compliance
        :param compliance_json:
        :return:
        """
        compliance_resources = []
        for compliance in compliance_json['members']:
            list_item = {}
            name = compliance['rule']['name']
            list_item["name"] = name[0:70] + '...'
            if compliance['status'] == 'NOT COMPLIANT':
                list_item["status"] = 'Non Compliant'
            elif compliance['status'] == "ERROR":
                list_item['status'] = "Failed"
            else:
                list_item["status"] = compliance['status'].title()
            list_item["key"] = compliance['policy']['name']
            compliance_resources.append(list_item)
        return compliance_resources

    def create_compliance_list(self, key, list):
        """
        Create a list of dictionary for compliance with the given status from compliance dictionary list
        :param key:
        :param list:
        :return:
        """
        compliance_list = []
        for item in list:
            item_list = {}
            if item['status'] == key:
                item_list['status'] = item['status'].title()
                item_list['name'] = item['name']
                item_list['key'] = item['key']
                compliance_list.append(item_list)
        return compliance_list

    def grab_compliance_resources_key_sorted_by_key(self, key_name, compliance_json):
        """
        Create a list of dictionary for compliance with specified key
        :param key_name:
        :param compliance_json:
        :return:
        """
        compliance_resources = []
        for compliance in compliance_json['members']:
            list_item = {}
            name = compliance['rule']['name']
            list_item["name"] = name[0:70] + '...'
            if compliance['status'] == 'NOT COMPLIANT':
                list_item["status"] = 'Non Compliant'
            elif compliance['status'] == "ERROR":
                list_item['status'] = "Failed"
            else:
                list_item["status"] = compliance['status'].title()
            if key_name == "Policy":
                list_item["key"] = compliance['policy']['name']
            if key_name == "Resource":
                list_item["key"] = compliance['resource']['name']
            if key_name == "Requirement":
                list_item["key"] = compliance['requirement']['name']
            compliance_resources.append(list_item)
        return compliance_resources

    def grab_compliance_resources_key_sorted_by_key_with_id(self, key_name, compliance_json):
        """
        Create a list of dictionary for compliance with specified key
        :param key_name:
        :param compliance_json:
        :return:
        """
        compliance_resources = []
        for compliance in compliance_json['members']:
            list_item = {}
            name = compliance['rule']['name']
            list_item["name"] = name[0:70] + '...'
            if compliance['status'] == 'NOT COMPLIANT':
                list_item["status"] = 'Non Compliant'
            elif compliance['status'] == "ERROR":
                list_item['status'] = "Failed"
            else:
                list_item["status"] = compliance['status'].title()
            if key_name == "Policy":
                list_item["key"] = compliance['policy']['name']
            if key_name == "Resource":
                list_item["key"] = compliance['resource']['name']
            if key_name == "Requirement":
                list_item["key"] = compliance['requirement']['name']
                list_item['id']=compliance['rule']['id']
            compliance_resources.append(list_item)
        return compliance_resources

    def grab_compliance_id_list(self, compliance_json):
        complice_id_list = []
        for compliance in compliance_json['members']:
            complice_id_list.append(compliance['rule']['id'])
        return complice_id_list

    def grab_compliance_details_list(self, compliance_json, compliance_id):
        """
        Create a list of dictionary for a specific compliance from compliance json
        :param compliance_json:
        :param compliance_id:
        :return:
        """
        compliance_resources = []
        for compliance in compliance_json['members']:
            list_item = {}
            if compliance['rule']['id'] == compliance_id:
                list_item['compliance_name'] = compliance['rule']['name']
                if compliance['status'] == "ERROR":
                    list_item['compliance_status'] = "Failed"
                elif compliance['status'] == "NOT COMPLIANT":
                    list_item['compliance_status'] = "Non Compliant"
                else:
                    list_item['compliance_status'] = compliance['status'].title()
                list_item['compliance_policy'] = compliance['policy']['name']
                list_item['compliance_requirement'] = compliance['requirement']['name']
                list_item['compliance_control'] = compliance['control']['name']
                compliance_resources.append(list_item)
        return compliance_resources


