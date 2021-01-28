from evictionfree.cover_letter import CoverLetterVariables
from evictionfree.hardship_declaration import HardshipDeclarationVariables
from django.contrib.auth.models import AnonymousUser
import freezegun
import pytest

from users.models import JustfixUser
from project.schema_base import (
    get_last_queried_phone_number,
    update_last_queried_phone_number,
    PhoneNumberAccountStatus,
)
from loc.tests.factories import LandlordDetailsV2Factory
from onboarding.schema import OnboardingStep1Info
from onboarding.tests.test_schema import _exec_onboarding_step_n
from norent.schema import update_scaffolding, SCAFFOLDING_SESSION_KEY
from users.tests.factories import UserFactory
from onboarding.tests.factories import OnboardingInfoFactory
from evictionfree.tests.factories import (
    HardshipDeclarationDetailsFactory,
    SubmittedHardshipDeclarationFactory,
)
from project.util.testing_util import one_field_err


class TestEvictionFreeCreateAccount:
    INCOMPLETE_ERR = [
        {"field": "__all__", "messages": ["You haven't completed all the previous steps yet."]}
    ]

    NYC_SCAFFOLDING = {
        "first_name": "zlorp",
        "last_name": "zones",
        "city": "New York City",
        "state": "NY",
        "email": "zlorp@zones.com",
    }

    NATIONAL_SCAFFOLDING = {
        "first_name": "boop",
        "last_name": "jones",
        "city": "Albany",
        "state": "NY",
        "email": "boop@jones.com",
        "street": "1200 Bingy Bingy Way",
        "apt_number": "5A",
        "zip_code": "12345",
    }

    @pytest.fixture(autouse=True)
    def setup_fixture(self, db, graphql_client):
        self.graphql_client = graphql_client

    def execute(self):
        input = {
            "password": "blarg1234",
            "confirmPassword": "blarg1234",
            "agreeToTerms": True,
            "canWeSms": True,
        }

        return self.graphql_client.execute(
            """
            mutation Create($input: EvictionFreeCreateAccountInput!) {
                output: evictionFreeCreateAccount(input: $input) {
                    errors { field, messages }
                    session {
                        firstName
                    }
                }
            }
            """,
            variables={"input": input},
        )["data"]["output"]

    def populate_phone_number(self):
        update_last_queried_phone_number(
            self.graphql_client.request, "5551234567", PhoneNumberAccountStatus.NO_ACCOUNT
        )

    def test_it_returns_error_when_session_is_empty(self):
        assert self.execute()["errors"] == self.INCOMPLETE_ERR

    def test_it_returns_error_when_only_phone_number_is_in_session(self):
        self.populate_phone_number()
        assert self.execute()["errors"] == self.INCOMPLETE_ERR

    def test_it_returns_error_when_nyc_addr_but_onboarding_step_1_empty(self):
        self.populate_phone_number()
        update_scaffolding(self.graphql_client.request, self.NYC_SCAFFOLDING)
        assert self.execute()["errors"] == self.INCOMPLETE_ERR

    def test_it_returns_error_when_national_addr_but_incomplete_scaffolding(self):
        self.populate_phone_number()
        scaff = {**self.NATIONAL_SCAFFOLDING, "street": ""}
        update_scaffolding(self.graphql_client.request, scaff)
        assert self.execute()["errors"] == self.INCOMPLETE_ERR

    def test_it_returns_error_when_national_addr_but_no_phone_number(self):
        update_scaffolding(self.graphql_client.request, self.NATIONAL_SCAFFOLDING)
        assert self.execute()["errors"] == self.INCOMPLETE_ERR

    def test_it_works_for_national_users(self):
        request = self.graphql_client.request
        self.populate_phone_number()
        update_scaffolding(request, self.NATIONAL_SCAFFOLDING)
        assert SCAFFOLDING_SESSION_KEY in request.session
        assert self.execute()["errors"] == []
        user = JustfixUser.objects.get(phone_number="5551234567")
        assert user.first_name == "boop"
        assert user.last_name == "jones"
        assert user.email == "boop@jones.com"
        oi = user.onboarding_info
        assert oi.non_nyc_city == "Albany"
        assert oi.borough == ""
        assert oi.state == "NY"
        assert oi.zipcode == "12345"
        assert oi.address == "1200 Bingy Bingy Way"
        assert oi.apt_number == "5A"
        assert oi.agreed_to_norent_terms is False
        assert oi.agreed_to_justfix_terms is False
        assert oi.agreed_to_evictionfree_terms is True

        assert oi.can_we_sms is True
        assert oi.can_rtc_sms is True
        assert oi.can_hj4a_sms is True

        assert get_last_queried_phone_number(request) is None
        assert SCAFFOLDING_SESSION_KEY not in request.session

    def test_it_works_for_nyc_users(self, smsoutbox, mailoutbox):
        request = self.graphql_client.request
        self.populate_phone_number()
        res = _exec_onboarding_step_n(1, self.graphql_client)
        assert OnboardingStep1Info.get_dict_from_request(request) is not None
        assert res["errors"] == []
        update_scaffolding(request, self.NYC_SCAFFOLDING)
        assert SCAFFOLDING_SESSION_KEY in request.session
        assert self.execute()["errors"] == []
        user = JustfixUser.objects.get(phone_number="5551234567")
        assert user.first_name == "zlorp"
        assert user.last_name == "zones"
        assert user.email == "zlorp@zones.com"
        oi = user.onboarding_info
        assert oi.non_nyc_city == ""
        assert oi.borough == "MANHATTAN"
        assert oi.state == "NY"
        assert oi.address == "123 boop way"
        assert oi.apt_number == "3B"
        assert oi.agreed_to_norent_terms is False
        assert oi.agreed_to_justfix_terms is False
        assert oi.agreed_to_evictionfree_terms is True

        # This will only get filled out if geocoding is enabled, which it's not.
        assert oi.zipcode == ""

        assert get_last_queried_phone_number(request) is None
        assert OnboardingStep1Info.get_dict_from_request(request) is None
        assert SCAFFOLDING_SESSION_KEY not in request.session


class TestEvictionFreeSubmitDeclaration:
    QUERY = """
    mutation {
        evictionFreeSubmitDeclaration(input: {}) {
            errors { field, messages }
        }
    }
    """

    @pytest.fixture(autouse=True)
    def setup_fixture(self, graphql_client, db):
        self.user = UserFactory(email="boop@jones.net")
        graphql_client.request.user = self.user
        self.graphql_client = graphql_client

    def create_landlord_details(self):
        LandlordDetailsV2Factory(user=self.user, email="landlordo@calrissian.net")

    def execute(self):
        res = self.graphql_client.execute(self.QUERY)
        return res["data"]["evictionFreeSubmitDeclaration"]

    def test_it_requires_login(self):
        self.graphql_client.request.user = AnonymousUser()
        assert self.execute()["errors"] == one_field_err(
            "You do not have permission to use this form!"
        )

    def test_it_raises_err_when_declaration_already_sent(self):
        SubmittedHardshipDeclarationFactory(user=self.user)
        assert self.execute()["errors"] == one_field_err(
            "You have already sent a hardship declaration!"
        )

    def test_it_raises_err_when_no_onboarding_info_exists(self):
        assert self.execute()["errors"] == one_field_err("You have not onboarded!")

    def test_it_raises_err_when_no_landlord_details_exist(self):
        OnboardingInfoFactory(user=self.user)
        assert self.execute()["errors"] == one_field_err(
            "You haven't provided any landlord details yet!"
        )

    def test_it_raises_err_when_no_hardship_declaration_details_exist(self):
        self.create_landlord_details()
        OnboardingInfoFactory(user=self.user)
        assert self.execute()["errors"] == one_field_err(
            "You have not provided details for your hardship declaration yet!"
        )

    def test_it_raises_err_when_user_is_outside_ny(self):
        self.create_landlord_details()
        OnboardingInfoFactory(user=self.user, state="CA")
        assert self.execute()["errors"] == one_field_err(
            "You must be in the state of New York to use this tool!"
        )

    def test_it_raises_err_when_used_on_wrong_site(self):
        self.create_landlord_details()
        OnboardingInfoFactory(user=self.user)
        HardshipDeclarationDetailsFactory(user=self.user)
        assert self.execute()["errors"] == one_field_err(
            "This form can only be used from the EvictionFreeNY site."
        )

    def test_it_works(
        self,
        use_evictionfree_site,
        fake_fill_hardship_pdf,
        settings,
        allow_lambda_http,
        mailoutbox,
        mocklob,
    ):
        settings.IS_DEMO_DEPLOYMENT = False
        self.create_landlord_details()
        OnboardingInfoFactory(user=self.user)
        HardshipDeclarationDetailsFactory(user=self.user)

        with freezegun.freeze_time("2021-01-26"):
            assert self.execute()["errors"] == []

        decl = self.user.submitted_hardship_declaration
        hd_vars = HardshipDeclarationVariables(**decl.declaration_variables)
        cl_vars = CoverLetterVariables(**decl.cover_letter_variables)

        assert cl_vars.date == "01/26/2021"
        assert hd_vars.name == "Boop Jones"
        assert decl.locale == "en"
        assert "Landlordo" in decl.cover_letter_html
        assert decl.mailed_at is not None
        assert decl.emailed_at is not None
        assert decl.emailed_to_housing_court_at is not None
        assert decl.emailed_to_user_at is not None
        assert decl.tracking_number == mocklob.sample_letter["tracking_number"]
        assert decl.lob_letter_object is not None

        assert len(mailoutbox) == 3

        ll_mail = mailoutbox[0]
        assert ll_mail.to == ["landlordo@calrissian.net"]
        assert "TODO: set email to landlord body" in ll_mail.body

        hc_mail = mailoutbox[1]
        assert hc_mail.to == ["KingsHardshipDeclaration@nycourts.gov"]
        assert "TODO: set email to housing court body" in hc_mail.body

        user_mail = mailoutbox[2]
        assert user_mail.to == ["boop@jones.net"]
        assert "Congratulations" in user_mail.body
