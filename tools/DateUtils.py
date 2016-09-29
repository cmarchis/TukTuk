import datetime

class DateUtils(object):
    def convert_long_to_date(self, long_date):
        """
        Convert a date (long) to a desired date format
        :param long_date:
        :return: formatted date
        """
        format = "%B %d, %Y"
        converted_date = datetime.datetime.fromtimestamp(long_date / 1e3)
        return converted_date.strftime(format)
