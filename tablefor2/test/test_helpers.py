import datetime

from django.test import TestCase

from tablefor2.helpers import determine_ampm, get_next_weekday, get_string_for_and_format


class HelpersTestCase(TestCase):
    def test_determine_ampm(self):
        self.assertEqual(determine_ampm('12:00PM'), '12:00')
        self.assertEqual(determine_ampm('5:00PM'), '17:00')
        self.assertEqual(determine_ampm('1:00PM'), '13:00')
        self.assertEqual(determine_ampm('10:00AM'), '10:00')
        self.assertEqual(determine_ampm('9:30AM'), '9:30')

    def test_get_next_weekday(self):
        today = datetime.datetime(2017, 8, 21)
        self.assertEqual(get_next_weekday(today, '0', '12:00'), datetime.datetime(2017, 8, 28, 12, 0))
        self.assertEqual(get_next_weekday(today, '1', '1:00'), datetime.datetime(2017, 8, 29, 1, 0))
        self.assertEqual(get_next_weekday(today, '4', '15:30'), datetime.datetime(2017, 9, 1, 15, 30))

        today = datetime.datetime(2017, 8, 24)
        self.assertEqual(get_next_weekday(today, '0', '12:00'), datetime.datetime(2017, 8, 28, 12, 0))
        self.assertEqual(get_next_weekday(today, '1', '1:00'), datetime.datetime(2017, 8, 29, 1, 0))
        self.assertEqual(get_next_weekday(today, '4', '15:30'), datetime.datetime(2017, 9, 1, 15, 30))

    def test_get_string_for_and_format(self):
        group = ['test 1', 'test 2', 'test 3', 'test 4'] # should return 'test 1, test 2, test 3, and test 4'
        array_len = len(group)
        self.assertEqual(get_string_for_and_format(group[0], 0, array_len), 'test 1, ')
        self.assertEqual(get_string_for_and_format(group[1], 1, array_len), 'test 2, ')
        self.assertEqual(get_string_for_and_format(group[2], 2, array_len), 'test 3, ')
        self.assertEqual(get_string_for_and_format(group[3], 3, array_len), 'and test 4.')
