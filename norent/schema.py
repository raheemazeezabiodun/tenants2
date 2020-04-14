import graphene
from graphql import ResolveInfo

from project import schema_registry
from project.util.session_mutation import SessionFormMutation
from . import scaffolding, forms


SCAFFOLDING_SESSION_KEY = f'norent_scaffolding_v{scaffolding.VERSION}'


class NorentScaffolding(graphene.ObjectType):
    '''
    Represents all fields of our scaffolding model.
    '''

    first_name = graphene.String(required=True)

    last_name = graphene.String(required=True)

    street = graphene.String(required=True)

    city = graphene.String(required=True)

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


@schema_registry.register_session_info
class NorentSessionInfo(object):
    norent_scaffolding = graphene.Field(NorentScaffolding)

    def resolve_norent_scaffolding(self, info: ResolveInfo):
        request = info.context
        kwargs = request.session.get(SCAFFOLDING_SESSION_KEY, {})
        if kwargs:
            return scaffolding.NorentScaffolding(**kwargs)
        return None


class NorentScaffoldingMutation(SessionFormMutation):
    class Meta:
        abstract = True

    @classmethod
    def perform_mutate(cls, form, info: ResolveInfo):
        request = info.context
        scaffolding_dict = request.session.get(SCAFFOLDING_SESSION_KEY, {})
        scaffolding_dict.update(form.cleaned_data)
        request.session[SCAFFOLDING_SESSION_KEY] = scaffolding_dict
        return cls.mutation_success()


@schema_registry.register_mutation
class NorentTenantInfo(NorentScaffoldingMutation):
    class Meta:
        form_class = forms.TenantInfo


@schema_registry.register_mutation
class NorentLandlordInfo(NorentScaffoldingMutation):
    class Meta:
        form_class = forms.LandlordInfo