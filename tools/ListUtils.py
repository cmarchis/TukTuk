from __future__ import division
from tools.ApiUtils import ApiUtils
from tools.DateUtils import DateUtils
from decimal import *


class ListUtils(object):
    def sort_list_alphabetically_by(self, field_key, list):
        """
        Sort provided list by the values of the given field_key
        :return sorted_list:
        """
        sorted_list = sorted(list, key=lambda k: k[field_key])
        return sorted_list

    def remove_duplicates_from_list(self, list):
        """
        Remove duplicated value from a list.
        :return: list with unique values
        """
        output = []
        seen = set()
        for value in list:
            if value not in seen:
                output.append(value)
                seen.add(value)
        return output

    def create_list_of_policies_model(self, policies_list, policies_type_list):
        """
        Create a minified list from the policies_list JSON
        :return: list(item[type, number, variances],...)
        """
        return_list = []
        for element in policies_type_list:
            list_item = {}
            list_item['type'] = element
            list_item['number'] = str(self.grab_total_of_same_policy_type(element, policies_list))
            list_item['variances'] = str(self.grab_variances(element, policies_list)) + " Variances"
            return_list.append(list_item)
        return return_list

    def create_list_of_policies_bar_dimensions(self, policies_type_list, policies_list, dimension):
        """
        For every policy type that is in policies list create a list of policies bar dimension
        :param dimension: the entire dimension of the bar
        :return:[{'blue': 57, 'gray': 36, 'type': u'Policy type', 'red': 72, 'yellow': 29},{...}]
        """
        return_list = []
        for element in policies_type_list:
            list_item = {}
            list_item['type'] = element
            total = self.return_total_compliant_value(element, policies_list)
            if self.grab_compliant_in_MSLO_of_same_policy_type(element, policies_list) != 0:
                actual = self.grab_compliant_in_MSLO_of_same_policy_type(element, policies_list)
                list_item['blue'] = self.value(self.percent(total, actual), dimension)
            if self.grab_noncompliant_in_RSLO_of_same_policy_type(element, policies_list) != 0:
                actual = self.grab_noncompliant_in_RSLO_of_same_policy_type(element, policies_list)
                list_item['yellow'] = self.value(self.percent(total, actual), dimension)
            if self.grab_noncompliant_out_RSLO_of_same_policy_type(element, policies_list) != 0:
                actual = self.grab_noncompliant_out_RSLO_of_same_policy_type(element, policies_list)
                list_item['red'] = self.value(self.percent(total, actual), dimension)
            if self.grab_unknown_of_same_policy_type(element, policies_list) != 0:
                actual = self.grab_unknown_of_same_policy_type(element, policies_list)
                list_item['gray'] = self.value(self.percent(total, actual), dimension)
            return_list.append(list_item)
        return return_list

    def grab_compliant_in_MSLO_of_same_policy_type(self, policy_type, policies_list):
        """
        Return 'compliant in MSLO' value for every policy type from policies_list
        """
        sum = 0
        for policy_now in policies_list:
            if policy_now['policyType']['name'] == policy_type:
                sum += policy_now['complianceScore']['compliantInMSLO']
        return sum

    def grab_noncompliant_in_RSLO_of_same_policy_type(self, policy_type, policies_list):
        """
        Return 'noncompliant in RSLO' value for every policy type from policies_list
        """
        sum = 0
        for policy_now in policies_list:
            if policy_now['policyType']['name'] == policy_type:
                sum += policy_now['complianceScore']['noncompliantInRSLO']
        return sum

    def grab_noncompliant_out_RSLO_of_same_policy_type(self, policy_type, policies_list):
        """
         Return 'noncompliant out RSLO' value for every policy type from policies_list
        """
        sum = 0
        for policy_now in policies_list:
            if policy_now['policyType']['name'] == policy_type:
                sum += policy_now['complianceScore']['noncompliantOutRSLO']
        return sum

    def grab_unknown_of_same_policy_type(self, policy_type, policies_list):
        """
        Return 'unknown' value for every policy type from policies_list
        """
        sum = 0
        for policy_now in policies_list:
            if policy_now['policyType']['name'] == policy_type:
                sum += policy_now['complianceScore']['unknown']
        return sum

    def return_total_compliant_value(self, policy_type, policies_list):
        """
        Return total compliant value for every policy type in policies_list
        """
        sum = self.grab_compliant_in_MSLO_of_same_policy_type(policy_type,
                                                              policies_list) + self.grab_noncompliant_in_RSLO_of_same_policy_type(
            policy_type, policies_list) + self.grab_noncompliant_out_RSLO_of_same_policy_type(policy_type,
                                                                                              policies_list) + self.grab_unknown_of_same_policy_type(
            policy_type, policies_list)
        return sum

    def percent(self, total, actual):
        """
         Return the percent of a specific compliant from the entire compliant score percentage
        :param total: total score
        :param actual: actual score for specific compliant
        :return:
        """
        procent = (float(actual) * 100) / float(total)
        return procent

    def value(self, percent, dimension):
        """
        Return the value of each bar by calculating it considering the percent of compliant and the entire dimension of bar
        :param percent:percent of compliant
        :param dimension:entire dimension of bar
        :return: dimension of bar
        """
        val = ((dimension * percent) / 100)
        val2 = int(val)
        val = val2 + 1
        return val

    def grab_variances(self, policy_type, policies_list):
        """
        From the policies list, return the total tests (from complianceScore) for policies with the same type
        """
        sum = 0
        for policy_now in policies_list:
            if policy_now['policyType']['name'] == policy_type:
                sum += policy_now['complianceScore']['noncompliantInRSLO'] + policy_now['complianceScore'][
                    'noncompliantOutRSLO']
        return sum

    def grab_list_of_policies_types(self, policies_list):
        """
        From policies list, return the list of policy type names
        :return: list(policy_name,...)
        """
        list = []
        for policy_now in policies_list:
            if policy_now['policyType']['name'] != None:
                list.append(policy_now['policyType']['name'])
        return list

    def grab_total_of_same_policy_type(self, policy_type, policies_list):
        """
        From the policies list, return the number of policies items with the same type
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
        :return list(item[name],...):
        """
        return_list = []
        for template_now in templtes_list:
            # list_item = {}
            # list_item['name'] = template_now['template']['template']['templateName']
            return_list.append(template_now['template']['template']['templateName'])

        return return_list

    def grab_template_data(self, template_name, templtes_list):
        """
        Grabbes template date as displayed on the template details page.
        :param template_name:
        :param templtes_list:
        :return item{resourceTypes[],attachedPolicies[],noOfDeployments}:
        """
        policy_details = {}
        for template_now in templtes_list:

            if template_now['template']['template']['templateName'] == template_name:
                resource_types = []
                for resource_now in template_now['template']['template']['resourceTypes']:
                    resource_types.append(resource_now['resourceName'])
                policy_details['resourceTypes'] = resource_types

                policies_list = []
                for policy_now in template_now['template']['template']['attachedPolicies']:
                    policies_list.append(policy_now['policy']['name'])
                policy_details['attachedPolicies'] = policies_list

                policy_details['noOfDeployments'] = template_now['noOfDeployments']

        return policy_details

    def grab_list_of_deployment_info(self, json):
        """
        From json grabbed from api, returns a list of deployment info
        :return: list{'status': 'SUCCESS','template': 'Oracle', 'last_scanned':'September 26, 2016'}
        """
        list_item = {}
        list_item['status'] = json['deployment']['status']
        list_item['template'] = json['deployment']['templateName']
        list_item['last_scanned'] = DateUtils().convert_long_to_date(json['deployment']['complianceScore'][
                                                                         'lastScanDate'])
        return list_item


if __name__ == "__main__":
    policies_list = ApiUtils().grab_policies_json()
    policies_json = ApiUtils().grab_json()
    templates_list = ApiUtils().grab_templates_json()

    print "aaa: ", ListUtils().create_list_of_policies_bar_dimensions(['Best practices', 'Practices'], policies_list,
                                                                      192)
