import urllib2, json


class MockPoliciesApiUtils(object):

    def grab_policy_json(self, api_url):
        request = urllib2.Request(api_url + '/policy')
        response = urllib2.urlopen(request)
        json_object = json.load(response)
        return json_object

    def grab_requirements_by_policy_id(self, api_url, policy_id):
        request = urllib2.Request(api_url + '/policy/' + policy_id + '/requirement')
        response = urllib2.urlopen(request)
        json_object = json.load(response)
        return json_object

    def grab_policy_requirement_tree_by_policy_id(self, api_url, policy_id):
        request = urllib2.Request(api_url + '/policy/' + policy_id + '/requirement_tree')
        response = urllib2.urlopen(request)
        json_object = json.load(response)
        return json_object