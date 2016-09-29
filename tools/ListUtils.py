from tools.ApiUtils import ApiUtils


class ListUtils(object):
    def sort_list_alphabetically_by(self, field_key, list):
        """
        Sort provided list by the values of the given field
        :param field_key:
        :param list:
        :return sorted_list:
        """
        sorted_list = sorted(list, key=lambda k: k[field_key])
        return sorted_list

    def remove_duplicates_from_list(self, list):
        output = []
        seen = set()
        for value in list:
            if value not in seen:
                output.append(value)
                seen.add(value)
        return output

    def create_list_of_policies_model(self, policies_list):
        """
        Create a minified list from the policies_list JSON
        :param policies_list:
        :return: list(item[type, number, variances],...)
        """
        list_of_policies_types = self.grab_list_of_policies_types(policies_list)
        return_list = []
        for element in list_of_policies_types:
            list_item = {}
            list_item['type'] = element
            list_item['number'] = str(self.grab_total_of_same_policy_type(element, policies_list))
            list_item['variances'] = str(self.grab_total(element, policies_list) - self.grab_undefined_policies(element,
                                                                                                                policies_list)) + " Variances"
            return_list.append(list_item)
        return return_list

    def grab_total(self, policy_type, policies_list):
        """
        From the policies list, return the total tests from policies with the same type
        :param policy_type:
        :param policies_list:
        :return: total
        """
        sum = 0
        for policy_now in policies_list:
            if policy_now['policyType']['name'] == policy_type:
                sum += policy_now['complianceScore']['totalTests']
        return sum

    def grab_list_of_policies_types(self, policies_list):
        """
        From policies list, return the list of policy type names
        :param policies_list:
        :return: list(policy_name,...)
        """
        list = []
        for policy_now in policies_list:
            if policy_now['policyType']['name'] != None:
                list.append(policy_now['policyType']['name'])
        # for policy_now in policies_list:
        #     if policy_now['policyType']['name'] != None:
        #         list.append(policy_now['policyType']['name'])
        return list

    def grab_total_of_same_policy_type(self, policy_type, policies_list):
        """
        From the policies list, return the number of policies items with the same type
        :param policy_type:
        :param policies_list:
        :return: total
        """
        sum = 0
        for policy_now in policies_list:
            if policy_now['policyType']['name'] == policy_type:
                sum += 1
        return sum

    def grab_undefined_policies(self, policy_type, policies_list):
        """
        From the policies list, return the total of undefined policies with the same type
        :param policy_type:
        :param policies_list:
        :return: total
        """
        sum = 0
        for policy_now in policies_list:
            if policy_now['policyType']['name'] == policy_type:
                sum += policy_now['complianceScore']['unknown']

        return sum

    def grab_list_of_resources_with_status(self, policies_list):
        """
        From list of policies, returns a list of resource name into correct compliance category
        :param policies_list:
        :return list(item[name, status],...):
        """
        return_list = []
        for policy_now in policies_list:
            list_item = {}
            list_item['name'] = policy_now['name']
            if policy_now['complianceScore']['unknown'] != 0:
                list_item['status'] = "Unknown"
            elif policy_now['complianceScore']['noncompliantOutRSLO'] != 0:
                list_item['status'] = "Non Compliant"
            elif policy_now['complianceScore']['noncompliantInRSLO'] != 0:
                list_item['status'] = "Warning"
            elif policy_now['complianceScore']['compliantInMSLO'] != 0:
                list_item['status'] = "Compliant"

            return_list.append(list_item)
        return return_list

    def grab_template_names(self, templtes_list):
        """
        From list of templates, returns a list of template names as a result
        :param policies_list:
        :return list(item[name],...):
        """
        return_list = []
        for template_now in templtes_list:
            list_item = {}
            list_item['name'] = template_now['templateName']
            return_list.append(list_item)

        return return_list

    def grab_template_data(self, template_name, templtes_list):
        list_item = {}
        for template_now in templtes_list:

            if template_now['templateName'] == template_name:
                list_item[]


        return list_item

if __name__ == "__main__":
    policies_list = ApiUtils().grab_policies_json()
    templates_list = ApiUtils().grab_templates_json()
    # print "aaa: ", ListUtils().grab_list_of_policies_types(policies_list)
    # list_of_policies_types = ListUtils().grab_list_of_policies_types(policies_list)
    # for element in list_of_policies_types:
    #     print"grab_undefined_policies:" ,ListUtils().grab_undefined_policies(element, policies_list)
    # print"aaa: ", ListUtils().grab_list_of_policies_types(policies_list)
    # print"aaa: ", ListUtils().grab_total_of_same_policy_type('Best practices', policies_list)
    # print"grab_total: ", ListUtils().grab_total('Best practices', policies_list)
    # print"grab_undefined_policies: ", ListUtils().grab_undefined_policies('Best practices', policies_list)

    print 'template names: ', ListUtils().grab_template_names(templates_list)