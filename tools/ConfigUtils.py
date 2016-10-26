import os

PROPERTY_SEPARATOR = '='
COMMENT_SEPARATOR = '#'
RUN_CONFIG_FILE = 'RunOption.txt'
path_root = os.path.dirname(os.path.dirname(__file__))


class ConfigUtils(object):
    """
    Read files from config folder. Will read from RunOption the desired config file. If none is selected it will default
    to dev.

    """
    def read_run_config(self):
        try:
            with open(os.path.join(path_root, 'configs', RUN_CONFIG_FILE), 'r') as f:
                return f.readline()
        except:
            pass
        return 'dev'

    def read_config_file(self):
        """
        Will return a dictionary with all properties read from a config file
        :return:
        """
        config_file_name = self.read_run_config().replace('\n', '');
        full_path = os.path.join(path_root, 'configs', config_file_name + '.ini')
        props = {}
        with open(full_path, 'rt') as f:
            for line in f:
                l = line.strip()
                if l and not l.startswith(COMMENT_SEPARATOR):
                    key_value = l.split(PROPERTY_SEPARATOR)
                    key = key_value[0].strip()
                    value = PROPERTY_SEPARATOR.join(key_value[1:]).strip('" \t')
                    props[key] = value
        return props
