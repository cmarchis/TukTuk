from datetime import datetime
from datetime import timedelta


class DateUtils(object):
    def convert_long_to_aplication_format_date(self, long_date):
        """
        Convert a date (long) to a desired date format
        :param long_date:
        :return: formatted date
        """
        format = "%B %d, %Y"
        converted_date = datetime.fromtimestamp(long_date / 1e3)
        return converted_date.strftime(format)

    def convert_long_y_m_d(self, long_date):
        """
        Convert a date (long) to a desired date format
        :param long_date:
        :return: formatted date
        """
        format = "%Y-%m-%d"
        converted_date = datetime.fromtimestamp(long_date / 1e3)
        return converted_date.strftime(format)

    def date_between(self, resource_date, start_date, end_date):
        return resource_date >= start_date and resource_date <= end_date

    def get_date_before_current_date(self, days_to_subtract):
        d = datetime.today() - timedelta(days=days_to_subtract)
        return d.strftime('%Y-%m-%d')


if __name__ == "__main__":
    print "aa: ", DateUtils().date_between('2016-09-26', '2016-09-26', '2016-09-26')
    print "aaa: ", DateUtils().get_date_before_current_date(7)
    a = DateUtils().convert_long_y_m_d(1476781116641)
    print a
