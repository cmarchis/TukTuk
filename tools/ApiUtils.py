import urllib, urllib2, json



class ApiUtils(object):
    """
    API calls to the GUI Rest API. These are used as expected data for validation
    """

    def grab_policies_json(self):
        """
        Return a json containing all policies from live api
        :return:
        """

        url = 'http://localhost:8010/urest/v1/deployments/d10c819a-0fb1-4910-8747-38ccb5f7f3e3'
        request = urllib2.Request(url)
        request.add_header('User-Agent', 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)')
        request.add_header('Content-Type', 'application/json')
        response = urllib2.urlopen(request)
        json_object = json.load(response)
        # print json_object['deployment']['attachedPolicy']
        my_policies = []

        for item_now in json_object['deployment']['attachedPolicy']:
            my_policies.append(item_now['policy'])

        return my_policies

    def grab_total(self, policy_type):
        my_policies = self.grab_policies_json()
        sum = 0
        for policy_now in my_policies:
            if policy_now['policyType']['name'] == policy_type:
                sum += policy_now['complianceScore']['totalTests']
        return sum

    def grab_list_of_policies_types(self):
        my_policies = self.grab_policies_json()
        list = []
        for policy_now in my_policies:
            if policy_now['policyType']['name'] != None:
                list.append(policy_now['policyType']['name'])
        return list

    def grab_total_of_same_policy_type(self, policy_type):
        my_policies = self.grab_policies_json()
        sum = 0
        for policy_now in my_policies:
            if policy_now['policyType']['name'] == policy_type:
                sum += 1
        return sum

    def grab_undefined_policies(self, policy_type):
        my_policies = self.grab_policies_json()
        sum = 0
        for policy_now in my_policies:
            if policy_now['policyType']['name'] == policy_type:
                sum += policy_now['complianceScore']['unknown']

        return sum


