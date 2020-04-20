import pytest

from django.core.management import call_command, CommandError
from norent.management.commands.pull_norent_airtable import (
    Table,
    convert_rows_to_state_dict
)


class TestConvertRowsToStateDict:
    @pytest.mark.parametrize('raw_rows,state_dict', [
        ([], {}),
        (
            [{'fields': {'ID': 1, 'State': 'WV', 'Boop': 2}}],
            {'WV': {'Boop': 2}}
        ),
        (
            [{'fields': {'State': 'WV', 'Boop': 2}}],
            {'WV': {'Boop': 2}}
        ),
        (
            [{'fields': {}}],
            {}
        ),
    ])
    def test_it_works(self, raw_rows, state_dict):
        result = convert_rows_to_state_dict(Table.DOCUMENTATION_REQUIREMENTS, raw_rows)
        assert result == state_dict


def test_it_raises_error_if_airtable_is_not_configured():
    with pytest.raises(CommandError, match='AIRTABLE_API_KEY'):
        call_command('pull_norent_airtable')