import urllib, urllib2, json

policies_url = 'http://localhost:8010/urest/v1/deployments/d10c819a-0fb1-4910-8747-38ccb5f7f3e3'

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

if __name__ == "__main__":
    print "grab_policies_json: ", ApiUtils().grab_policies_json()
