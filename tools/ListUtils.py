from tools.ApiUtils import ApiUtils


class ListUtils(object):
    def remove_duplicates_from_list(self, list):
        output = []
        seen = set()
        for value in list:
            if value not in seen:
                output.append(value)
                seen.add(value)
        return output

    def create_list_of_policies_model(self, list_of_policies_types):
        return_list = []
        for element in list_of_policies_types:
            list_item = {}
            list_item['type'] = element
            list_item['number'] = ApiUtils().grab_total_of_same_policy_type(element)
            list_item['variances'] = ApiUtils().grab_total(element) - ApiUtils().grab_undefined_policies(element)
            return_list.append(list_item)
        return return_list


if __name__ == "__main__":
    print "list: ", ListUtils().create_list_of_policies_model(
        ListUtils().remove_duplicates_from_list(ApiUtils().grab_list_of_policies_types()))
