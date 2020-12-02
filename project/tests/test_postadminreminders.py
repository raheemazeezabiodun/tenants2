from io import StringIO
import freezegun
from django.core.management import call_command

from loc.tests.factories import LetterRequestFactory


class TestPostAdminReminders:
    def test_it_posts_reminders_for_old_loc_requests(self, db):
        output = StringIO()
        with freezegun.freeze_time("2001-01-01"):
            LetterRequestFactory()
        call_command("postadminreminders", stdout=output)
        assert "Posting reminder to admins about sending letters of complaint" in output.getvalue()

    def test_it_ignores_new_loc_requests(self, db):
        output = StringIO()
        LetterRequestFactory()
        call_command("postadminreminders", stdout=output)
        assert "No reminders need to be posted" in output.getvalue()
