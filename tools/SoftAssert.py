
class SoftAssert(object):
    """
    The class will handle multiple assertions and for each failure will save the error message in the failures list.
    This list if not empty failures have been found during assertions.
    """
    _failures = []

    def clean_failures(self, list_of_failures):
        """
        Clear the list of failures.
        :param list_of_failures:
        :return:
        """
        for itemNow in list_of_failures:
            list_of_failures.remove(itemNow)

    def verfy_equals_true(self, message, expected, actual):
        if expected != actual:
            self._failures.append(message + 'Expected: |' + format(expected) + '| - Actual: |' + format(actual) + '|')

    def verfy_contains_true(self, message, expected, actual):
        if expected not in actual:
            self._failures.append(message + 'Expected: |' + expected + '| - Actual: |' + actual + '|')

    def verify_all_elements_are_present(self, expected_list, actual_list):
        """
        Verifies that the two lists contain all elements. This method does not take into account ordering.
        :param expected_list:
        :param actual_list:
        :return:
        """
        for expected_item in expected_list:
            expected_is_found = False
            for actual_item in actual_list:
                if expected_item == actual_item:
                    expected_is_found = True
                    break

            if expected_is_found == False:
                self._failures.append('Expected item was not found in list. Expected: ' + format(
                    expected_item) + ' \n ActualList: ' + format(actual_list))

    def failures_size(self):
        return len(self._failures)

    def failures_list(self):
        return self._failures
