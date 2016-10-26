import os
import ast

PROPERTY_SEPARATOR = '='
COMMENT_SEPARATOR = '#'
LIST_SEPARATOR = ','

class FileUtils(object):

    """
    The class is used to read data files from the data folder.
    """
    def read_property(self, file_name, property_name):
        """
        Provided a file name and a property name, it will return the value of that property
        :param file_name:
        :param property_name:
        :return:
        """
        path_root = os.path.dirname(os.path.dirname(__file__))
        with open(os.path.join(path_root, 'data', file_name), 'rt') as f:
            property_value = ''
            for line in f:
                l = line.strip()
                if l and not l.startswith(COMMENT_SEPARATOR):
                    key_value = l.split(PROPERTY_SEPARATOR)
                    key = key_value[0].strip()
                    if property_name == key:
                        return PROPERTY_SEPARATOR.join(key_value[1:]).strip(' \t')
                        break
            return property_value

    def read_properties_as_list(self, file_name, property_name):
        return self.read_property(file_name, property_name).split(LIST_SEPARATOR)

    def read_properties_as_dictionary(self, file_name, property_name):
        dictionary_list = ast.literal_eval(self.read_property(file_name, property_name))
        return list(dictionary_list)
