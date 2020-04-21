from typing import Optional, Dict, Any
import graphene
from graphql import ResolveInfo
from graphene_django.types import DjangoObjectType

from project import schema_registry
from project.util.session_mutation import SessionFormMutation
from project.schema_base import get_last_queried_phone_number
from onboarding.schema import OnboardingStep1Info, complete_onboarding
from onboarding.models import SIGNUP_INTENT_CHOICES
from loc.models import LandlordDetails
from . import scaffolding, forms, models


SCAFFOLDING_SESSION_KEY = f'norent_scaffolding_v{scaffolding.VERSION}'


class NorentScaffolding(graphene.ObjectType):
    '''
    Represents all fields of our scaffolding model.
    '''

    first_name = graphene.String(required=True)

    last_name = graphene.String(required=True)

    street = graphene.String(required=True)

    city = graphene.String(required=True)

    is_city_in_nyc = graphene.Boolean()

    state = graphene.String(required=True)

    zip_code = graphene.String(required=True)

    apt_number = graphene.String(required=True)

    email = graphene.String(required=True)

    phone_number = graphene.String(required=True)

    landlord_name = graphene.String(required=True)

    landlord_primary_line = graphene.String(required=True)

    landlord_city = graphene.String(required=True)

    landlord_state = graphene.String(required=True)

    landlord_zip_code = graphene.String(required=True)

    landlord_email = graphene.String(required=True)

    landlord_phone_number = graphene.String(required=True)

    def resolve_is_city_in_nyc(self, info: ResolveInfo) -> Optional[bool]:
        return self.is_city_in_nyc()


class NorentLetter(DjangoObjectType):
    class Meta:
        model = models.Letter
        only_fields = ('tracking_number', 'letter_sent_at')

    payment_date = graphene.Date(
        required=True,
        description="The rent payment date the letter is for.",
        resolver=lambda self, info: self.rent_period.payment_date
    )


class NorentRentPeriod(DjangoObjectType):
    class Meta:
        model = models.RentPeriod
        only_fields = ('payment_date',)


@schema_registry.register_session_info
class NorentSessionInfo(object):
    norent_scaffolding = graphene.Field(NorentScaffolding)

    norent_latest_rent_period = graphene.Field(
        NorentRentPeriod,
        description="The latest rent period one can create a no rent letter for.")

    norent_latest_letter = graphene.Field(
        NorentLetter,
        description=(
            "The latest no rent letter sent by the user. If the user has never "
            "sent a letter or is not logged in, this will be null."
        ),
    )

    def resolve_norent_latest_rent_period(self, info: ResolveInfo):
        return models.RentPeriod.objects.first()

    def resolve_norent_latest_letter(self, info: ResolveInfo):
        request = info.context
        if not request.user.is_authenticated:
            return None
        return models.Letter.objects.filter(user=request.user).first()

    def resolve_norent_scaffolding(self, info: ResolveInfo):
        request = info.context
        kwargs = request.session.get(SCAFFOLDING_SESSION_KEY, {})
        if kwargs:
            return scaffolding.NorentScaffolding(**kwargs)
        return None


def get_scaffolding(request) -> scaffolding.NorentScaffolding:
    scaffolding_dict = request.session.get(SCAFFOLDING_SESSION_KEY, {})
    return scaffolding.NorentScaffolding(**scaffolding_dict)


def update_scaffolding(request, new_data):
    scaffolding_dict = request.session.get(SCAFFOLDING_SESSION_KEY, {})
    scaffolding_dict.update(new_data)
    request.session[SCAFFOLDING_SESSION_KEY] = scaffolding_dict


class NorentScaffoldingMutation(SessionFormMutation):
    class Meta:
        abstract = True

    @classmethod
    def perform_mutate(cls, form, info: ResolveInfo):
        request = info.context
        update_scaffolding(request, form.cleaned_data)
        return cls.mutation_success()


@schema_registry.register_mutation
class NorentLandlordInfo(NorentScaffoldingMutation):
    class Meta:
        form_class = forms.LandlordInfo


@schema_registry.register_mutation
class NorentFullName(NorentScaffoldingMutation):
    class Meta:
        form_class = forms.FullName


@schema_registry.register_mutation
class NorentCityState(NorentScaffoldingMutation):
    class Meta:
        form_class = forms.CityState


@schema_registry.register_mutation
class NorentNationalAddress(NorentScaffoldingMutation):
    class Meta:
        form_class = forms.NationalAddress


@schema_registry.register_mutation
class NorentEmail(NorentScaffoldingMutation):
    class Meta:
        form_class = forms.Email


def are_all_truthy(*args) -> bool:
    for arg in args:
        if not arg:
            return False
    return True


def scaffolding_to_landlord_details(request):
    scf = get_scaffolding(request)
    if not scf.landlord_name:
        return None
    details = LandlordDetails(
        name=scf.landlord_name,
        email=scf.landlord_email,
        primary_line=scf.landlord_primary_line,
        city=scf.landlord_city,
        state=scf.landlord_state,
        zip_code=scf.landlord_zip_code,
    )
    details.address = '\n'.join(details.address_lines_for_mailing)
    return details


@schema_registry.register_mutation
class NorentSendLetter(SessionFormMutation):
    login_required = True

    @classmethod
    def send_letter(cls, request, ld: LandlordDetails, rp: models.RentPeriod):
        user = request.user
        html_content = "<p>TODO: Render HTML of letter in React.</p>"
        letter = models.Letter(
            user=user,
            rent_period=rp,
            html_content=html_content,
        )
        letter.full_clean()
        letter.save()

        if ld.email:
            # TODO: Send letter via email.
            pass

        if ld.primary_line:
            user_addr = user.onboarding_info.as_lob_params()
            addr_details = ld.get_or_create_address_details_model()
            ll_addr = addr_details.as_lob_params()
            print(user_addr, ll_addr)
            # TODO: Mail letter via lob.

    @classmethod
    def perform_mutate(cls, form, info: ResolveInfo):
        request = info.context
        user = request.user
        assert user.is_authenticated
        rent_period = models.RentPeriod.objects.first()
        if not rent_period:
            return cls.make_error("No rent periods are defined!")
        letter = models.Letter.objects.filter(user=user, rent_period=rent_period).first()
        if letter is not None:
            return cls.make_error("You have already sent a letter for this rent period!")
        if not hasattr(user, 'onboarding_info'):
            return cls.make_error("You have not onboarded!")

        ld = scaffolding_to_landlord_details(request)

        if not ld:
            return cls.make_error("You haven't provided any landlord details yet!")

        cls.send_letter(request, ld, rent_period)

        return cls.mutation_success()


@schema_registry.register_mutation
class NorentCreateAccount(SessionFormMutation):
    class Meta:
        form_class = forms.CreateAccount

    @classmethod
    def fill_nyc_info(cls, request, info: Dict[str, Any]):
        step1 = OnboardingStep1Info.get_dict_from_request(request)
        if step1 is None:
            return None
        info['borough'] = step1['borough']
        info['address'] = step1['address']
        info['apt_number'] = step1['apt_number']
        info['address_verified'] = step1['address_verified']
        return info

    @classmethod
    def fill_city_info(cls, request, info: Dict[str, Any], scf: scaffolding.NorentScaffolding):
        if scf.is_city_in_nyc():
            return cls.fill_nyc_info(request, info)

        if not are_all_truthy(scf.street, scf.zip_code, scf.apt_number):
            return None
        info['non_nyc_city'] = scf.city
        info['address'] = scf.street
        info['apt_number'] = scf.apt_number
        info['zipcode'] = scf.zip_code
        info['address_verified'] = False
        return info

    @classmethod
    def get_previous_step_info(cls, request) -> Optional[Dict[str, Any]]:
        scf = get_scaffolding(request)
        phone_number = get_last_queried_phone_number(request)
        if not are_all_truthy(
            phone_number, scf.first_name, scf.last_name, scf.city,
            scf.state, scf.email
        ):
            return None
        info: Dict[str, Any] = {
            'phone_number': phone_number,
            'first_name': scf.first_name,
            'last_name': scf.last_name,
            'state': scf.state,
            'email': scf.email,
            'signup_intent': SIGNUP_INTENT_CHOICES.NORENT,
        }
        return cls.fill_city_info(request, info, scf)

    @classmethod
    def perform_mutate(cls, form, info: ResolveInfo):
        request = info.context
        password = form.cleaned_data['password']
        allinfo = cls.get_previous_step_info(request)
        if allinfo is None:
            cls.log(info, "User has not completed previous steps, aborting mutation.")
            return cls.make_error("You haven't completed all the previous steps yet.")
        allinfo.update(form.cleaned_data)
        complete_onboarding(request, info=allinfo, password=password)

        # TODO: Remove data from session.

        return cls.mutation_success()
