from django import forms

from project.forms import SetPasswordForm, UniqueEmailForm, ensure_at_least_one_is_true
from project.util.mailing_address import (
    US_STATE_CHOICES, ZipCodeValidator, CITY_KWARGS)
from project.util.address_form_fields import (
    ADDRESS_FIELD_KWARGS)
from project.util.phone_number import USPhoneNumberField
from loc.models import LandlordDetails
from onboarding.models import OnboardingInfo, APT_NUMBER_KWARGS
from users.models import JustfixUser


class LandlordInfo(forms.Form):
    '''
    Corresponds to fields in our scaffolding model that
    involve landlord info.
    '''

    landlord_name = forms.CharField()

    # e.g. "666 FIFTH AVENUE, APT 2"
    landlord_primary_line = forms.CharField()

    landlord_city = forms.CharField()

    landlord_state = forms.ChoiceField(choices=US_STATE_CHOICES.choices)

    landlord_zip_code = forms.CharField()

    landlord_email = forms.EmailField(required=False)

    landlord_phone_number = USPhoneNumberField(required=False)


class FullName(forms.ModelForm):
    class Meta:
        model = JustfixUser
        fields = ('first_name', 'last_name')


class CityState(forms.Form):
    city = forms.CharField(**CITY_KWARGS)

    state = forms.ChoiceField(choices=US_STATE_CHOICES.choices)


class NationalAddress(forms.Form):
    street = forms.CharField(**ADDRESS_FIELD_KWARGS)

    apt_number = forms.CharField(**APT_NUMBER_KWARGS)

    zip_code = forms.CharField(validators=[ZipCodeValidator()])


class Email(UniqueEmailForm):
    pass


class CreateAccount(SetPasswordForm, forms.ModelForm):
    class Meta:
        model = OnboardingInfo
        fields = ('can_we_sms',)

    agree_to_terms = forms.BooleanField(required=True)


class LandlordNameAndContactTypes(forms.ModelForm):
    class Meta:
        model = LandlordDetails
        fields = ('name',)

    has_email_address = forms.BooleanField(required=False)

    has_mailing_address = forms.BooleanField(required=False)

    def clean(self):
        return ensure_at_least_one_is_true(super().clean())
