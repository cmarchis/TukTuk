class ResourceListUtils(object):
    def grab_resource_dictionary_list(self, resource_json):
        resource_list = []
        for resource in resource_json['members']:
            resource_data = {}
            resource_data['resourceId'] = resource['resourceId']
            resource_data['resourceName'] = resource['resourceName']
            resource_data['templateName'] = resource['templateName']
            resource_list.append(resource_data)
        return resource_list

    def grab_compliance_list_from_resource_id_compliance_json(self, resource_compliance_json):
        compliance_list = []
        for compliance in resource_compliance_json:
            compliance_data = {}
            if compliance['complianceStatus'] == "ERROR":
                compliance_data['status'] = "Failed"
            elif compliance['complianceStatus'] == "NOT COMPLIANT":
                compliance_data['status'] = "Non Compliant"
            elif compliance['complianceStatus'] == "NOT MEASURED":
                compliance_data['status'] = "Unknown"
            else:
                compliance_data['status'] = compliance['complianceStatus'].title()
            compliance_data['id'] = compliance['rule']['id']
            compliance_data['name'] = compliance['rule']['name']
            compliance_list.append(compliance_data)
        return compliance_list

    def grab_compliance_details_from_resource_id_compliance_json(self, resource_compliance_json, compliance_id):
        compliance_details_list = []
        for compliance in resource_compliance_json:
            if compliance['rule']['id'] == compliance_id:
                compliance_data = {}
                compliance_data['name'] = compliance['rule']['name']
                if compliance['complianceStatus'] == "ERROR":
                    compliance_data['status'] = "Failed"
                elif compliance['complianceStatus'] == "NOT COMPLIANT":
                    compliance_data['status'] = "Non Compliant"
                elif compliance['complianceStatus'] == "NOT MEASURED":
                    compliance_data['status'] = "Unknown"
                else:
                    compliance_data['status'] = compliance['complianceStatus'].title()
                compliance_data['policy'] = compliance['policy']['name']
                compliance_data['requirement'] = compliance['requirement']['name']
                compliance_data['control'] = compliance['control']['name']
                compliance_details_list.append(compliance_data)
        return compliance_details_list

    def grab_resource_info_from_resource_json(self, resource_json, resource_id):
        resource_data = {}
        for resource in resource_json['members']:
            if resource['resourceId'] == resource_id:
                resource_data['template'] = resource['templateName']
                resource_data['deployment'] = resource['deploymentName']
        return resource_data

    def grab_compliance_score_for_resource(self, deployment_resouces_json, resource_id):
        compliant_score = {}
        for resource in deployment_resouces_json['resources']:
            if resource['resourceId'] == resource_id:
                compliant_score['compliance'] = str(resource['complianceScore']['compliantInMSLO']) + ' of ' + \
                                                str(resource['complianceScore']['totalTests']) + ' Compliant'
        return compliant_score

    def grab_deployment_id_by_resource_id_from_resource_json(self, resource_json, resource_id):
        deployment_id = ''
        for resource in resource_json['members']:
            if resource['resourceId'] == resource_id:
                deployment_id = resource['deploymentId']
        return deployment_id

    def grab_credential_list(self, credential_resource_id_json):
        credential_list = []
        for credential in credential_resource_id_json:
            credential_list.append(credential['name'])
            return credential_list
