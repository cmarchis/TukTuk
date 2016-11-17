from random import randint


class StringUtils(object):
    def generate_random_string_number(self, number):
        random_sring_number = str(randint(0, number))
        return random_sring_number
