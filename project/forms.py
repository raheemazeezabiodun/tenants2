from typing import Optional
from django import forms
from django.forms import ValidationError
from django.contrib.auth import authenticate

from users.models import PHONE_NUMBER_LEN, JustfixUser
from project.common_data import Choices
from project import geocoding


BOROUGH_CHOICES = Choices.from_file('borough-choices.json')

LEASE_CHOICES = Choices.from_file('lease-choices.json')


class USPhoneNumberField(forms.CharField):
    '''
    A field for a United States phone number.
    '''

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 15  # Allow for extra characters, we'll remove them.
        super().__init__(*args, **kwargs)

    def clean(self, value: str) -> str:
        cleaned = super().clean(value)
        cleaned = ''.join([
            ch for ch in cleaned
            if ch in '1234567890'
        ])
        if len(cleaned) == PHONE_NUMBER_LEN + 1 and cleaned.startswith('1'):
            # The user specified the country calling code, remove it.
            cleaned = cleaned[1:]
        if len(cleaned) != PHONE_NUMBER_LEN:
            raise ValidationError(
                'This does not look like a U.S. phone number. '
                'Please include the area code, e.g. 555-123-4567.'
            )
        return cleaned


class OnboardingStep1Form(forms.Form):
    name = forms.CharField(max_length=100)

    address = forms.CharField(max_length=200)

    borough = forms.ChoiceField(choices=BOROUGH_CHOICES)

    apt_number = forms.CharField(max_length=10)

    def clean(self):
        cleaned_data = super().clean()
        address = cleaned_data.get('address')
        borough = cleaned_data.get('borough')
        if address and borough:
            features = geocoding.search(', '.join([address, borough]))
            if features is None:
                # Hmm, the geocoding service is unavailable. This
                # is unfortunate, but we don't want it to block
                # onboarding, so keep a note of it and let the
                # user continue.
                address_verified = False
            elif len(features) == 0:
                # The geocoding service is available, but the
                # address produces no results.
                raise forms.ValidationError('The address provided is invalid.')
            else:
                address_verified = True
                address = features[0].properties.name
            cleaned_data['address'] = address
            cleaned_data['address_verified'] = address_verified
        return cleaned_data


class OnboardingStep2Form(forms.Form):
    is_in_eviction = forms.BooleanField(
        required=False,
        help_text="Has the user received an eviction notice?")

    needs_repairs = forms.BooleanField(
        required=False,
        help_text="Does the user need repairs in their apartment?")

    has_no_services = forms.BooleanField(
        required=False,
        help_text="Is the user missing essential services like water?")

    has_pests = forms.BooleanField(
        required=False,
        help_text="Does the user have pests like rodents or bed bugs?")

    has_called_311 = forms.BooleanField(
        required=False,
        help_text="Has the user called 311 before?")


class OnboardingStep3Form(forms.Form):
    lease_type = forms.ChoiceField(choices=LEASE_CHOICES)

    receives_public_assistance = forms.BooleanField(
        required=False,
        help_text="Does the user receive public assistance, e.g. Section 8?")


class LoginForm(forms.Form):
    phone_number = USPhoneNumberField()

    password = forms.CharField()

    # This will be set to a valid user once is_valid() returns True.
    authenticated_user: Optional[JustfixUser] = None

    def clean(self):
        cleaned_data = super().clean()
        phone_number = cleaned_data.get('phone_number')
        password = cleaned_data.get('password')

        if phone_number and password:
            user = authenticate(phone_number=phone_number, password=password)
            if user is None:
                raise ValidationError('Invalid phone number or password.',
                                      code='authenticate_failed')
            self.authenticated_user = user
