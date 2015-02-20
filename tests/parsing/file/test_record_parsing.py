# -*- encoding: utf-8 -*-
import unittest

from pyparsing import ParseException

from cwr.parsing.record import RecordPrefixDecoder


"""
CWR record parsing tests.

The following cases are tested:
- RecordPrefixDecoder decodes correctly formatted record prefixes

- RecordPrefixDecoder throws an exception when the record type is not one of the CWR record types
- RecordPrefixDecoder throws an exception when the record numbers are too short
- RecordPrefixDecoder throws an exception when the record numbers are too long
"""

__author__ = 'Bernardo Martínez Garrido'
__license__ = 'MIT'
__version__ = '0.0.0'
__status__ = 'Development'


class TestParseRecordPrefixValid(unittest.TestCase):
    """
    Tests that RecordPrefixDecoder decodes correctly formatted strings
    """

    def setUp(self):
        self._parser = RecordPrefixDecoder()

    def test_valid(self):
        """
        Tests that RecordPrefixDecoder decodes correctly formatted record prefixes.
        """
        prefix = 'HDR0000123400000023'

        result = self._parser.decode(prefix)

        self.assertEqual('HDR', result.record_type)
        self.assertEqual(1234, result.transaction_sequence_n)
        self.assertEqual(23, result.record_sequence_n)


class TestParseRecordPrefixException(unittest.TestCase):
    """
    Tests that RecordPrefixDecoder throws exceptions with incorrectly formatted strings.
    """

    def setUp(self):
        self._parser = RecordPrefixDecoder()

    def test_invalid_wrong_type(self):
        """
        Tests that RecordPrefixDecoder throws an exception when the record type is not one of the CWR record types.
        """
        prefix = 'AAA0000123400000023'

        self.assertRaises(ParseException, self._parser.decode, prefix)

    def test_invalid_wrong_length_too_short(self):
        """
        Tests that RecordPrefixDecoder throws an exception when the record numbers are too short.
        """
        prefix = 'HDR000123400000023'

        self.assertRaises(ParseException, self._parser.decode, prefix)

    def test_invalid_wrong_length_too_long_record_n(self):
        """
        Tests that RecordPrefixDecoder throws an exception when the record numbers are too long.
        """
        prefix = 'HDR00000123400000023'

        self.assertRaises(ParseException, self._parser.decode, prefix)

    def test_invalid_wrong_length_too_long_begin_space(self):
        """
        Tests that RecordPrefixDecoder throws an exception when the prefix is headed by empty spaces.
        """
        prefix = ' HDR0000123400000023'

        self.assertRaises(ParseException, self._parser.decode, prefix)