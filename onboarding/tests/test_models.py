import datetime
from django.core.exceptions import ValidationError
import pytest

from users.tests.factories import UserFactory
from .factories import OnboardingInfoFactory
from onboarding.models import OnboardingInfo
from project.tests.test_geocoding import enable_fake_geocoding, EXAMPLE_SEARCH


class TestBuildingLinks:
    def test_it_works_when_empty(self):
        info = OnboardingInfo()
        assert info.building_links == []
        assert info.get_building_links_html() == ''

    def test_it_shows_wow_link_when_bbl_is_present(self):
        info = OnboardingInfo(pad_bbl='1234')
        assert 'Who Owns What' in info.get_building_links_html()

    def test_it_shows_bis_link_when_bin_is_present(self):
        info = OnboardingInfo(pad_bin='1234')
        assert 'DOB BIS' in info.get_building_links_html()


def test_str_works_when_fields_are_not_set():
    info = OnboardingInfo()
    assert str(info) == 'OnboardingInfo object (None)'


def test_str_works_when_fields_are_set():
    info = OnboardingInfo(user=UserFactory.build(),
                          created_at=datetime.datetime(2018, 1, 2))
    assert str(info) == "Boop Jones's onboarding info from Tuesday, January 02 2018"


def test_borough_label_works():
    info = OnboardingInfo()
    assert info.borough_label == ''

    info.borough = 'STATEN_ISLAND'
    assert info.borough_label == 'Staten Island'

    info.borough = 'MANHATTAN'
    assert info.borough_label == 'Manhattan'


def test_city_works():
    info = OnboardingInfo()
    assert info.city == ''

    info.non_nyc_city = "Beetville"
    assert info.city == "Beetville"

    info.non_nyc_city = ""
    info.borough = 'STATEN_ISLAND'
    assert info.city == 'Staten Island'

    info.borough = 'MANHATTAN'
    assert info.city == 'New York'


@pytest.mark.parametrize('kwargs,match', [
    (dict(state='ZZ'), "not a valid choice"),
    (dict(zipcode='abcde'), "Enter a valid U.S. zip code"),
    (dict(borough="MANHATTAN", non_nyc_city="Beetville"),
     "One cannot be in an NYC borough and outside NYC simultaneously"),
])
def test_validation_errors_are_raised(db, kwargs, match):
    onb = OnboardingInfoFactory(**kwargs)
    with pytest.raises(ValidationError, match=match):
        onb.full_clean()


@pytest.mark.parametrize('kwargs', [
    dict(),
    dict(zipcode='43210'),
    dict(borough='MANHATTAN', non_nyc_city=""),
    dict(borough='', non_nyc_city="Beetville"),
])
def test_validation_errors_are_not_raised(db, kwargs):
    onb = OnboardingInfoFactory(**kwargs)
    onb.full_clean()


def test_full_nyc_address_works():
    info = OnboardingInfo()
    assert info.full_nyc_address == ''

    info.borough = 'STATEN_ISLAND'
    assert info.full_nyc_address == ''

    info.address = '123 Boop street'
    assert info.full_nyc_address == '123 Boop street, Staten Island'


def test_address_lines_for_mailing():
    info = OnboardingInfo()
    assert info.address_lines_for_mailing == []

    info.address = "150 Boop Way"
    assert info.address_lines_for_mailing == ["150 Boop Way"]

    info.apt_number = "2"
    assert info.address_lines_for_mailing == ["150 Boop Way", "Apartment 2"]

    info.borough = "MANHATTAN"
    info.state = "NY"
    assert info.address_lines_for_mailing == ["150 Boop Way", "Apartment 2", "New York, NY"]

    info.zipcode = "11201"
    assert info.address_lines_for_mailing == ["150 Boop Way", "Apartment 2", "New York, NY 11201"]

    info.borough = ""
    info.non_nyc_city = "Beetville"
    info.state = "OH"
    info.zipcode = "43210"
    assert info.address_lines_for_mailing == ["150 Boop Way", "Apartment 2", "Beetville, OH 43210"]


class TestAddrMetadataLookup:
    def mkinfo(self, **kwargs):
        return OnboardingInfo(
            address='150 court street',
            borough='BROOKLYN',
            **kwargs
        )

    def mkinfo_without_metadata(self):
        return self.mkinfo()

    def mkinfo_with_metadata(self):
        return self.mkinfo(zipcode='11231', pad_bbl='2002920026', pad_bin='1000000')

    def test_no_lookup_when_full_address_is_empty(self):
        assert OnboardingInfo().maybe_lookup_new_addr_metadata() is False

    def test_no_lookup_when_address_is_non_nyc(self):
        onb = OnboardingInfo(
            address='1 Boop Way',
            non_nyc_city="Beetville",
            state="OH",
            zipcode="43215",
        )
        assert onb.maybe_lookup_new_addr_metadata() is False
        assert onb.zipcode == "43215"

    def test_no_lookup_when_addr_and_metadata_have_changed(self):
        info = self.mkinfo_with_metadata()
        info.address = '120 zzz street'
        info.zipcode = '12345'
        info.pad_bbl = '4002920026'
        info.pad_bin = '4000000'
        assert info.maybe_lookup_new_addr_metadata() is False

    def test_no_lookup_when_metadata_exists_and_nothing_changed(self):
        info = self.mkinfo_with_metadata()
        assert info.maybe_lookup_new_addr_metadata() is False

    def test_lookup_when_addr_is_same_but_metadata_is_empty(self):
        info = self.mkinfo_without_metadata()
        assert info.maybe_lookup_new_addr_metadata() is True

    def test_lookup_when_addr_changes_and_geocoding_fails(self):
        info = self.mkinfo_with_metadata()
        info.address = 'times square'
        assert info.maybe_lookup_new_addr_metadata() is True
        assert info.zipcode == ''
        assert info.pad_bbl == ''
        assert info.pad_bin == ''

        # Because geocoding failed, we should always try looking up
        # new metadata, in case geocoding works next time.
        assert info.maybe_lookup_new_addr_metadata() is True

    @enable_fake_geocoding
    def test_lookup_when_addr_changes_and_geocoding_works(self, requests_mock, settings):
        info = self.mkinfo_with_metadata()
        info.address = 'times square'
        requests_mock.get(settings.GEOCODING_SEARCH_URL, json=EXAMPLE_SEARCH)
        assert info.maybe_lookup_new_addr_metadata() is True

        # Make sure we "remember" that our metadata is associated with
        # our new address, i.e. we don't think we need to look it up again.
        assert info.maybe_lookup_new_addr_metadata() is False

    def test_lookup_when_borough_changes(self):
        info = self.mkinfo_with_metadata()
        info.borough = 'MANHATTAN'
        assert info.maybe_lookup_new_addr_metadata() is True

    @enable_fake_geocoding
    def test_successful_lookup_is_applied_to_model(self, requests_mock, settings):
        requests_mock.get(settings.GEOCODING_SEARCH_URL, json=EXAMPLE_SEARCH)
        info = self.mkinfo_without_metadata()
        assert info.maybe_lookup_new_addr_metadata() is True
        assert info.zipcode == '11201'
        assert info.pad_bbl == '3002920026'
        assert info.pad_bin == '3003069'
