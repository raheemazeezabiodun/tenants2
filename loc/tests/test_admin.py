import pytest

from users.models import JustfixUser
from users.tests.factories import UserFactory
from users.tests.test_admin_user_proxy import UserProxyAdminTester
from project.tests.util import strip_locale
from loc.admin import (
    LetterRequestInline,
    print_loc_envelopes,
    get_lob_nomail_reason,
    LetterRequestForm,
)
from loc.admin_views import LocAdminViews
from loc.models import LetterRequest, LOC_MAILING_CHOICES
from . import lob_fixture
from .test_forms import save_letter_request_form
from .test_views import requires_pdf_rendering
from .factories import LandlordDetailsFactory, LetterRequestFactory, create_user_with_all_info


def test_loc_actions_shows_text_when_user_has_no_letter_request():
    lr = LetterRequest()
    assert LetterRequestInline.loc_actions(None, lr) == (
        "This user has not yet completed the letter of complaint process."
    )


@pytest.mark.django_db
def test_loc_actions_shows_pdf_link_when_user_has_letter_request():
    user = UserFactory()
    lr = LetterRequest(user=user)
    lr.save()
    assert f"/loc/admin/{user.pk}/letter.pdf" in LetterRequestInline.loc_actions(None, lr)


@pytest.mark.django_db
def test_print_loc_envelopes_works():
    user = UserFactory()
    redirect = print_loc_envelopes(None, None, JustfixUser.objects.all())
    url = strip_locale(redirect.url)
    assert url == f"/loc/admin/envelopes.pdf?user_ids={user.pk}"


@pytest.mark.django_db
def test_letter_request_form_creates_html_content_upon_creation(allow_lambda_http):
    form1 = save_letter_request_form(form_class=LetterRequestForm)
    lr = form1.instance
    assert "generated by a staff member" in lr.html_content
    assert lr.user.first_name.upper() in lr.html_content.upper()

    lr.user.first_name = "IT CHANGED!"
    lr.user.save()

    save_letter_request_form(form_class=LetterRequestForm, instance=lr)
    assert lr.user.first_name.upper() not in lr.html_content.upper()


class TestLobIntegrationField:
    def lob_integration(self, obj):
        return LetterRequestInline.lob_integration(None, obj)

    def test_it_returns_info_when_already_mailed(self):
        lr = LetterRequest()
        lr.lob_letter_object = lob_fixture.SAMPLE_LETTER
        assert self.lob_integration(lr) == (
            'The letter was <a href="https://dashboard.lob.com/#/letters/ltr_4868c3b754655f90" '
            'rel="noreferrer noopener" target="_blank">'
            "sent via Lob</a> with the tracking number 9407300000000000000004 and has an "
            "expected delivery date of 2017-09-12."
        )

    def test_it_returns_button_when_it_can_be_mailed(self, monkeypatch, db):
        lr = LetterRequestFactory()
        monkeypatch.setattr("loc.admin.get_lob_nomail_reason", lambda _: None)
        assert self.lob_integration(lr) == (
            f'<a class="button" href="/admin/lob/{lr.pk}/">'
            "Mail letter of complaint via Lob&hellip;</a>"
        )

    def test_it_returns_reason_when_it_cannot_be_mailed(self):
        assert (
            self.lob_integration(LetterRequest())
            == "Unable to send mail via Lob because Lob integration is disabled."
        )


def create_valid_letter_request():
    user = create_user_with_all_info()
    return LetterRequestFactory(user=user, html_content="<p>boop</p>")


class TestCreateMailConfirmationContext:
    deliverable = lob_fixture.get_sample_verification(deliverability="deliverable")
    deliverable_incorrect_unit = lob_fixture.get_sample_verification(
        deliverability="deliverable_incorrect_unit"
    )
    undeliverable = lob_fixture.get_sample_verification(deliverability="undeliverable")

    def create(self, landlord_verification, user_verification, is_manually_overridden=False):
        return LocAdminViews(None)._create_mail_confirmation_context(
            landlord_verification, user_verification, is_manually_overridden
        )

    def test_manual_override_works(self):
        ctx = self.create(self.undeliverable, self.undeliverable, False)
        assert ctx["is_deliverable"] is False
        assert ctx["is_manually_overridden"] is False

        ctx = self.create(self.undeliverable, self.undeliverable, True)
        assert ctx["is_deliverable"] is True
        assert ctx["is_manually_overridden"] is True

    @pytest.mark.parametrize(
        "landlord,user,expected",
        [
            [deliverable, undeliverable, True],
            [undeliverable, deliverable, False],
            [undeliverable, undeliverable, False],
            [deliverable_incorrect_unit, deliverable, True],
            [deliverable, deliverable, True],
        ],
    )
    def test_is_deliverable_works(self, landlord, user, expected):
        assert self.create(landlord, user)["is_deliverable"] is expected

    @pytest.mark.parametrize(
        "landlord,user,expected",
        [
            [deliverable, undeliverable, False],
            [undeliverable, deliverable, False],
            [deliverable_incorrect_unit, deliverable, False],
            [deliverable, deliverable, True],
        ],
    )
    def test_is_definitely_deliverable_works(self, landlord, user, expected):
        assert self.create(landlord, user)["is_definitely_deliverable"] is expected


class TestMailViaLob:
    @pytest.fixture(autouse=True)
    def setup_fixtures(self, db, mocklob):
        self.lr = create_valid_letter_request()
        self.url = f"/admin/lob/{self.lr.pk}/"

    def test_get_works(self, admin_client, mocklob):
        res = admin_client.get(self.url)
        assert res.status_code == 200
        assert b"Mail it with Lob!" in res.content

    @requires_pdf_rendering
    def test_post_works(self, admin_client, mocklob):
        signed_verifications = LocAdminViews(None)._create_mail_confirmation_context(
            landlord_verification=lob_fixture.get_sample_verification(),
            user_verification=lob_fixture.get_sample_verification(),
            is_manually_overridden=False,
        )["signed_verifications"]
        res = admin_client.post(self.url, data={"signed_verifications": signed_verifications})
        assert res.status_code == 200
        assert b"Hooray, the letter was sent via Lob" in res.content
        self.lr.refresh_from_db()
        assert self.lr.tracking_number == mocklob.sample_letter["tracking_number"]
        assert self.lr.lob_letter_object["carrier"] == "USPS"


class TestRejectLetter:
    @pytest.fixture(autouse=True)
    def setup_fixtures(self, db, mocklob):
        self.lr = create_valid_letter_request()
        self.url = f"/admin/reject/{self.lr.pk}/"

    def test_get_works(self, admin_client, mocklob):
        res = admin_client.get(self.url)
        assert res.status_code == 200
        assert b"Rejection reason" in res.content

    def test_post_raises_errors(self, admin_client):
        res = admin_client.post(self.url, data={"rejection_reason": "BOOP"})
        assert res.status_code == 200
        assert b"There was an error in your form submission" in res.content

    def test_post_works(self, admin_client):
        user = self.lr.user
        res = admin_client.post(
            self.url, data={"rejection_reason": "INCRIMINATION", "notes": "blah"}
        )
        assert res.status_code == 302
        with pytest.raises(LetterRequest.DoesNotExist):
            self.lr.refresh_from_db()
        alr = user.archived_letter_requests.all()
        assert len(alr) == 1
        assert alr[0].rejection_reason == "INCRIMINATION"
        assert alr[0].notes == "blah"


class TestArchiveLetter:
    @pytest.fixture(autouse=True)
    def setup_fixtures(self, db, mocklob):
        self.lr = create_valid_letter_request()
        self.url = f"/admin/archive/{self.lr.pk}/"

    def test_get_works(self, admin_client, mocklob):
        res = admin_client.get(self.url)
        assert res.status_code == 200
        assert b"Additional notes (optional)" in res.content

    def test_post_raises_errors(self, admin_client):
        res = admin_client.post(self.url, data={"notes": "BOOP" * 4000})
        assert res.status_code == 200
        assert b"There was an error in your form submission" in res.content

    def test_post_works(self, admin_client):
        user = self.lr.user
        res = admin_client.post(self.url, data={"notes": "blah"})
        assert res.status_code == 302
        with pytest.raises(LetterRequest.DoesNotExist):
            self.lr.refresh_from_db()
        alr = user.archived_letter_requests.all()
        assert len(alr) == 1
        assert alr[0].notes == "blah"


class TestGetLobNomailReason:
    def test_it_works_when_lob_integration_is_disabled(self):
        assert get_lob_nomail_reason(LetterRequest()) == "Lob integration is disabled"

    def test_it_works_when_letter_has_no_pk(self, mocklob):
        assert get_lob_nomail_reason(LetterRequest()) == "the letter has not yet been created"

    def test_it_works_when_letter_has_been_sent_manually(self, mocklob, db):
        lr = LetterRequestFactory(tracking_number="boop")
        assert get_lob_nomail_reason(lr) == "the letter has already been mailed manually"

    def test_it_works_when_letter_has_already_been_sent(self, mocklob, db):
        lr = LetterRequestFactory(lob_letter_object={"blah": 1})
        assert get_lob_nomail_reason(lr) == "the letter has already been sent via Lob"

    def test_it_works_when_we_rejected_the_letter(self, mocklob, db):
        lr = LetterRequestFactory(rejection_reason="letter contains gibberish")
        assert get_lob_nomail_reason(lr) == "we have rejected the letter"

    def test_it_works_when_user_mails_letter_themselves(self, mocklob, db):
        lr = LetterRequestFactory(mail_choice=LOC_MAILING_CHOICES.USER_WILL_MAIL)
        assert get_lob_nomail_reason(lr) == "the user wants to mail the letter themself"

    def test_it_works_when_user_has_no_landlord_details(self, mocklob, db):
        lr = LetterRequestFactory()
        assert get_lob_nomail_reason(lr) == "the user does not have landlord details"

    def test_it_works_when_user_has_no_onboarding_info(self, mocklob, db):
        lr = LetterRequestFactory()
        LandlordDetailsFactory(user=lr.user)
        assert get_lob_nomail_reason(lr) == "the user does not have onboarding info"

    def test_it_returns_none_when_letter_can_be_mailed_via_lob(self, mocklob, db):
        assert get_lob_nomail_reason(create_valid_letter_request()) is None


class TestLOCUserAdmin(UserProxyAdminTester):
    list_view_url = "/admin/loc/locuser/"

    def create_user(self):
        return LetterRequestFactory().user
