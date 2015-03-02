# -*- encoding: utf-8 -*-

from data.accessor import CWRTables, CWRConfiguration
from cwr.grammar import field, field_special, record, table
from cwr import work
from cwr.constraints import work as constraints


"""
CWR Work grammar.
"""

__author__ = 'Bernardo Martínez Garrido'
__license__ = 'MIT'
__version__ = '0.0.0'
__status__ = 'Development'

# Acquires data sources
_tables = CWRTables()
_config = CWRConfiguration()

"""
Work fields.
"""

# Work Title
work_title = field.alphanum(_config.field_size('work', 'work_title'), compulsory=True)
work_title = work_title.setName('Work Title').setResultsName('title')

# Submitter Work Number
work_id = field.alphanum(_config.field_size('work', 'work_id'), compulsory=True)
work_id = work_id.setName('Submitter Work Number').setResultsName('work_id')

# ISWC
iswc = field_special.iswc()
iswc = iswc.setName('ISWC').setResultsName('iswc')

# Copyright Date
copyright_date = field.date()
copyright_date = copyright_date.setName('Copyright Date').setResultsName('copyright_date')

# Copyright Number
copyright_number = field.alphanum(_config.field_size('work', 'copyright_number'))
copyright_number = copyright_number.setName('Copyright Number').setResultsName('copyright_number')

# Duration
duration = field.time()
duration = duration.setName('Duration').setResultsName('duration')

# Recorded Indicator
recorded = field.flag(compulsory=True)
recorded = recorded.setName('Recorded Indicator').setResultsName('recorded_indicator')

# Contact Name
contact_name = field.alphanum(_config.field_size('work', 'contact_name'))
contact_name = contact_name.setName('Contact Name').setResultsName('contact_name')

# Contact ID
contact_id = field.alphanum(_config.field_size('work', 'contact_id'))
contact_id = contact_id.setName('Contact ID').setResultsName('contact_id')

# Grand Rights Indicator
gr_indicator = field.boolean()
gr_indicator = gr_indicator.setName('Grand Rights Indicator').setResultsName('grand_rights_indicator')

# Composite Component Count
composite_count = field.numeric(_config.field_size('work', 'composite_count'))
composite_count = composite_count.setName('Composite Component Count').setResultsName('composite_component_count')

# Date of Publication of Printed Edition
printed_edition_publication_date = field.date()
printed_edition_publication_date = printed_edition_publication_date.setName(
    'Date of Publication of Printed Edition').setResultsName('printed_edition_publication_date')

# Exceptional Clause
exceptional_clause = field.flag()
exceptional_clause = exceptional_clause.setName('Exceptional Clause').setResultsName('exceptional_clause')

# Opus Number
opus_number = field.alphanum(_config.field_size('work', 'opus_number'))
opus_number = opus_number.setName('Opus Number').setResultsName('opus_number')

# Catalogue Number
catalogue_number = field.alphanum(_config.field_size('work', 'catalogue'))
catalogue_number = catalogue_number.setName('Catalogue Number').setResultsName('catalogue_number')

# Priority Flag
priority_flag = field.flag()
priority_flag = priority_flag.setName('Priority Flag').setResultsName('priority_flag')

"""
Work patterns.
"""

work_record = field_special.lineStart + record.record_prefix(_config.record_type('work')) + work_title + \
              table.language + work_id + iswc + \
              copyright_date + copyright_number + table.musical_distribution_category + duration + recorded + \
              table.text_music_relationship + table.composite_type + table.version_type + table.excerpt_type + table.music_arrangement + \
              table.lyric_adaptation + contact_name + contact_id + table.work_type + gr_indicator + composite_count + \
              printed_edition_publication_date + exceptional_clause + opus_number + catalogue_number + priority_flag + \
              field_special.lineEnd

"""
Parsing actions for the patterns.
"""

work_record.setParseAction(lambda p: _to_work(p))

"""
Validation actions for the patterns.
"""
work_record.addParseAction(lambda p: constraints.ser_has_duration(p[0]))
work_record.addParseAction(lambda p: constraints.mod_has_music_arrangement(p[0]))
work_record.addParseAction(lambda p: constraints.mod_has_lyric_adaptation(p[0]))
work_record.addParseAction(lambda p: constraints.composite_has_count(p[0]))
work_record.addParseAction(lambda p: constraints.count_when_composite(p[0]))

"""
Parsing methods.

These are the methods which transform nodes into instances of classes.
"""


def _to_work(parsed):
    """
    Transforms the final parsing result into a WorkRecord instance.

    :param parsed: result of parsing a Work transaction header
    :return: a WorkRecord created from the parsed record
    """
    return work.WorkRecord(parsed.record_type, parsed.transaction_sequence_n, parsed.record_sequence_n,
                           parsed.work_id, parsed.title, parsed.version_type, parsed.musical_distribution_category,
                           printed_edition_publication_date=parsed.printed_edition_publication_date,
                           text_music_relationship=parsed.text_music_relationship,
                           language_code=parsed.language,
                           copyright_number=parsed.copyright_number,
                           copyright_date=parsed.copyright_date,
                           music_arrangement=parsed.music_arrangement,
                           lyric_adaptation=parsed.lyric_adaptation,
                           excerpt_type=parsed.excerpt_type,
                           composite_type=parsed.composite_type,
                           composite_component_count=parsed.composite_component_count,
                           iswc=parsed.iswc,
                           cwr_work_type=parsed.cwr_work_type,
                           duration=parsed.duration,
                           catalogue_number=parsed.catalogue_number,
                           opus_number=parsed.opus_number,
                           contact_id=parsed.contact_id,
                           contact_name=parsed.contact_name,
                           recorded_indicator=parsed.recorded_indicator,
                           priority_flag=parsed.priority_flag,
                           exceptional_clause=parsed.exceptional_clause,
                           grand_rights_indicator=parsed.grand_rights_indicator)