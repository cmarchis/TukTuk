import urllib2, json


class MockComplianceApiUtils(object):
    def grab_compliance_json(self, api_url):
        """
        Return the json grabbed from api
        :return:
        """
        request = urllib2.Request(
            api_url + '/compliance/compliance_detail')
        response = urllib2.urlopen(request)
        json_object = json.load(response)
        return json_object

    def grab_sorted_ascending_compliance_json(self, api_url):
        """
        Return the json grabbed from api
        :return:
        """
        request = urllib2.Request(
            api_url + '/compliance/compliance_detail?&sort=requirement.name:asc')
        response = urllib2.urlopen(request)
        json_object = json.load(response)
        return json_object

    def grab_sorted_descending_compliance_json(self, api_url):
        """
        Return the json grabbed from api
        :return:
        """
        request = urllib2.Request(
            api_url + '/compliance/compliance_detail?&sort=requirement.name:desc')
        response = urllib2.urlopen(request)
        json_object = json.load(response)
        return json_object


