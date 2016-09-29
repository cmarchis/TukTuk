import urllib, urllib2, json

policies_url = 'http://localhost:8010/urest/v1/deployments/d10c819a-0fb1-4910-8747-38ccb5f7f3e3'
templates_url = 'http://localhost:8010/urest/v1/templates'

class ApiUtils(object):
    """
    API calls to the GUI Rest API. These are used as expected data for validation
    """

    def grab_policies_json(self):
        """
        Return a json containing all policies from live api
        :return:
        """
        request = urllib2.Request(policies_url)
        response = urllib2.urlopen(request)
        json_object = json.load(response)
        policies_list = []
        for item_now in json_object['deployment']['attachedPolicies']:
            policies_list.append(item_now['policy'])

        return policies_list

    def grab_templates_json(self):
        """
        Return a json containing all templates from live api
        :return:
        """
        request = urllib2.Request(templates_url)
        response = urllib2.urlopen(request)
        json_object = json.load(response)
        templates_list = []
        # print json_object['templates']['templateDeployments'][0]['template']['template']
        for item_now in json_object['templates']['templateDeployments']:
            templates_list.append(item_now['template']['template'])
        return templates_list


if __name__ == "__main__":
    print "grab_policies_json: ", ApiUtils().grab_policies_json()
    print "grab_templates_json: ", ApiUtils().grab_templates_json()
    print "grab_templates_json len: ", len(ApiUtils().grab_templates_json())
