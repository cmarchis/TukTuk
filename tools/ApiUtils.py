import urllib2, json
from decimal import *

policies_url = 'http://localhost:8010/urest/v1/deployments'
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

    def grab_json(self):
        """
        Return the json grabbed from api
        :return:
        """
        request = urllib2.Request(policies_url)
        response = urllib2.urlopen(request)
        json_object = json.load(response)
        return json_object

    def grab_templates_json(self):
        """
        Return a json containing all templates from live api
        :return:
        """
        request = urllib2.Request(templates_url)
        response = urllib2.urlopen(request)
        json_object = json.load(response)
        templates_list = []
        for item_now in json_object['templates']['templateDeployments']:
            templates_list.append(item_now)
        return templates_list

    def grab_job_json(self,deployment_id):
        """
        Return the json grabbed from api
        :return:
        """
        request = urllib2.Request('http://localhost:8010/urest/v1/deployments/'+deployment_id+'/job')
        response = urllib2.urlopen(request)
        json_object = json.load(response)
        return json_object



if __name__ == "__main__":
    # print "grab_policies_json: ", ApiUtils().grab_json()
    print "job : ", ApiUtils().grab_job_json('6170')
    # print "grab_templates_json: ", ApiUtils().grab_templates_json()
    # print "grab_templates_json len: ", len(ApiUtils().grab_templates_json())


