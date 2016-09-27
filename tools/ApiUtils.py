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
        myPolicies = []

        for item_now in json_object['deployment']['attachedPolicy']:
            myPolicies.append(item_now['policy'])
        print myPolicies
        print myPolicies[1]['name']

        return myPolicies