from typing import Optional, List
import graphene
from graphene_django.types import DjangoObjectType
from graphql import ResolveInfo
from django.urls import reverse
from django.forms import inlineformset_factory

from users.models import JustfixUser
from docusign.views import create_callback_url_for_signing_flow
from project.util.session_mutation import SessionFormMutation
from project.util.email_attachment import EmailAttachmentMutation
from project import schema_registry
from project.util.site_util import absolutify_url
from project.util.model_form_util import (
    ManyToOneUserModelFormMutation,
    OneToOneUserModelFormMutation,
    create_model_for_user_resolver,
    create_models_for_user_resolver
)
from project.util.django_graphql_forms import DjangoFormMutation
from issues.models import Issue
from .models import HPUploadStatus, COMMON_DATA, HPActionDocuments
import docusign.core
from . import models, forms, lhiapi, email_packet, docusign as hpadocusign


def sync_emergency_issues(user, submitted_issues: List[str]):
    for area, all_area_issues in forms.EMERGENCY_HPA_ISSUES_BY_AREA.items():
        user_area_issues = Issue.objects.get_area_issues_for_user(user, area)
        for issue in all_area_issues:
            sync_one_value(issue, issue in submitted_issues, user_area_issues)
        Issue.objects.set_area_issues_for_user(user, area, user_area_issues)


@schema_registry.register_mutation
class BeginDocusign(DjangoFormMutation):
    class Meta:
        form_class = forms.BeginDocusignForm

    login_required = True

    redirect_url = graphene.String()

    @classmethod
    def perform_mutate(cls, form, info: ResolveInfo):
        request = info.context
        user = request.user
        if not user.email:
            return cls.make_error("You have no email address!")

        # TODO: Ensure the user has validated their email address.

        docs = HPActionDocuments.objects.get_latest_for_user(user)

        if not docs:
            return cls.make_error("You have no HP Action documents to sign!")

        return_url = create_callback_url_for_signing_flow(
            request,
            absolutify_url(form.cleaned_data['next_url']),
        )
        envelope_definition = hpadocusign.create_envelope_definition_for_hpa(docs)
        api_client = docusign.core.create_default_api_client()
        _, url = hpadocusign.create_envelope_and_recipient_view_for_hpa(
            user=user,
            envelope_definition=envelope_definition,
            api_client=api_client,
            return_url=return_url,
        )

        return cls(errors=[], redirect_url=url)


@schema_registry.register_mutation
class EmailHpActionPdf(EmailAttachmentMutation):
    attachment_name = "an HP Action packet"

    @classmethod
    def send_email(cls, user_id: int, recipients: List[str]):
        email_packet.email_packet_async(user_id, recipients)

    @classmethod
    def perform_mutate(cls, form, info: ResolveInfo):
        latest = HPActionDocuments.objects.get_latest_for_user(info.context.user)
        if latest is None:
            return cls.make_error("You do not have an HP Action packet to send!")
        return super().perform_mutate(form, info)


def sync_one_value(value: str, is_value_present: bool, values: List[str]) -> List[str]:
    '''
    Makes sure that the given value either is or isn't in the given list.

    Destructively modifies the list in-place and returns it.

    Examples:

        >>> sync_one_value('boop', False, ['boop', 'jones'])
        ['jones']
        >>> sync_one_value('boop', True, ['boop', 'jones'])
        ['boop', 'jones']
        >>> sync_one_value('boop', True, ['jones'])
        ['jones', 'boop']
        >>> sync_one_value('boop', False, ['jones'])
        ['jones']
    '''

    if is_value_present and value not in values:
        values.append(value)
    if not is_value_present and value in values:
        values.remove(value)
    return values


@schema_registry.register_mutation
class EmergencyHPAIssues(SessionFormMutation):
    class Meta:
        form_class = forms.EmergencyHPAIssuesForm

    login_required = True

    @classmethod
    def perform_mutate(cls, form, info: ResolveInfo):
        user = info.context.user
        sync_emergency_issues(user, form.cleaned_data['issues'])
        details, _ = models.HPActionDetails.objects.get_or_create(user=user)
        details.sue_for_repairs = True
        details.sue_for_harassment = False
        details.save()
        return cls.mutation_success()


@schema_registry.register_mutation
class GenerateHpActionPdf(SessionFormMutation):
    class Meta:
        form_class = forms.GeneratePDFForm

    login_required = True

    @classmethod
    def perform_mutate(cls, form: forms.GeneratePDFForm, info: ResolveInfo):
        user = info.context.user
        token = models.UploadToken.objects.create_for_user(user)
        lhiapi.async_get_answers_and_documents_and_notify(token.id)
        return cls.mutation_success()


class FeeWaiverType(DjangoObjectType):
    class Meta:
        model = models.FeeWaiverDetails
        exclude_fields = ('user', 'id')


class HPActionDetailsType(DjangoObjectType):
    class Meta:
        model = models.HPActionDetails
        exclude_fields = ('user', 'id')


class HarassmentDetailsType(DjangoObjectType):
    class Meta:
        model = models.HarassmentDetails
        exclude_fields = ('user', 'id')


class TenantChildType(DjangoObjectType):
    class Meta:
        model = models.TenantChild
        exclude_fields = ('user', 'created_at', 'updated_at')


class PriorHPActionCaseType(DjangoObjectType):
    class Meta:
        model = models.PriorCase
        exclude_fields = ('user', 'created_at', 'updated_at')


@schema_registry.register_mutation
class FeeWaiverMisc(OneToOneUserModelFormMutation):
    class Meta:
        form_class = forms.FeeWaiverMiscForm


@schema_registry.register_mutation
class FeeWaiverIncome(OneToOneUserModelFormMutation):
    class Meta:
        form_class = forms.FeeWaiverIncomeForm


@schema_registry.register_mutation
class FeeWaiverExpenses(OneToOneUserModelFormMutation):
    class Meta:
        form_class = forms.FeeWaiverExpensesForm


@schema_registry.register_mutation
class FeeWaiverPublicAssistance(OneToOneUserModelFormMutation):
    class Meta:
        form_class = forms.FeeWaiverPublicAssistanceForm


@schema_registry.register_mutation
class HPActionPreviousAttempts(OneToOneUserModelFormMutation):
    class Meta:
        form_class = forms.PreviousAttemptsForm


@schema_registry.register_mutation
class HPActionUrgentAndDangerous(OneToOneUserModelFormMutation):
    class Meta:
        form_class = forms.UrgentAndDangerousForm


@schema_registry.register_mutation
class HPActionSue(OneToOneUserModelFormMutation):
    class Meta:
        form_class = forms.SueForm


@schema_registry.register_mutation
class HarassmentApartment(OneToOneUserModelFormMutation):
    class Meta:
        form_class = forms.HarassmentApartmentForm


@schema_registry.register_mutation
class HarassmentAllegations1(OneToOneUserModelFormMutation):
    class Meta:
        form_class = forms.HarassmentAllegations1Form


@schema_registry.register_mutation
class HarassmentAllegations2(OneToOneUserModelFormMutation):
    class Meta:
        form_class = forms.HarassmentAllegations2Form


@schema_registry.register_mutation
class HarassmentExplain(OneToOneUserModelFormMutation):
    class Meta:
        form_class = forms.HarassmentExplainForm


@schema_registry.register_mutation
class AccessForInspection(OneToOneUserModelFormMutation):
    class Meta:
        form_class = forms.AccessForInspectionForm

    @classmethod
    def perform_mutate(cls, form, *args, **kwargs):
        if form.instance.id is None:
            # Database constraints will be violated if we actually try saving this,
            # so just return a validation error for now. This should never really
            # happen unless a user created via the admin UI or command-line was made.
            return cls.make_error("You must complete onboarding before submitting this form!")
        return super().perform_mutate(form, *args, **kwargs)


@schema_registry.register_mutation
class TenantChildren(ManyToOneUserModelFormMutation):
    class Meta:
        formset_classes = {
            'children': inlineformset_factory(
                JustfixUser,
                models.TenantChild,
                forms.TenantChildForm,
                can_delete=True,
                max_num=COMMON_DATA['TENANT_CHILDREN_MAX_COUNT'],
                validate_max=True,
            )
        }


@schema_registry.register_mutation
class PriorHPActionCases(ManyToOneUserModelFormMutation):
    class Meta:
        formset_classes = {
            'cases': inlineformset_factory(
                JustfixUser,
                models.PriorCase,
                forms.PriorCaseForm,
                can_delete=True,
                max_num=10,
                validate_max=True,
            )
        }


@schema_registry.register_session_info
class HPActionSessionInfo:
    fee_waiver = graphene.Field(
        FeeWaiverType,
        resolver=create_model_for_user_resolver(models.FeeWaiverDetails)
    )

    hp_action_details = graphene.Field(
        HPActionDetailsType,
        resolver=create_model_for_user_resolver(models.HPActionDetails)
    )

    harassment_details = graphene.Field(
        HarassmentDetailsType,
        resolver=create_model_for_user_resolver(models.HarassmentDetails)
    )

    latest_hp_action_pdf_url = graphene.String(
        description=(
            "The URL of the most recently-generated HP Action PDF "
            "for the current user."
        )
    )

    hp_action_upload_status = graphene.Field(graphene.Enum.from_enum(HPUploadStatus),
                                             required=True,
                                             description=HPUploadStatus.__doc__)

    tenant_children = graphene.List(
        graphene.NonNull(TenantChildType),
        resolver=create_models_for_user_resolver(models.TenantChild)
    )

    prior_hp_action_cases = graphene.List(
        graphene.NonNull(PriorHPActionCaseType),
        resolver=create_models_for_user_resolver(models.PriorCase)
    )

    def resolve_latest_hp_action_pdf_url(self, info: ResolveInfo) -> Optional[str]:
        request = info.context
        if not request.user.is_authenticated:
            return None
        if models.HPActionDocuments.objects.filter(user=request.user).exists():
            return reverse('hpaction:latest_pdf')
        return None

    def resolve_hp_action_upload_status(self, info: ResolveInfo) -> HPUploadStatus:
        request = info.context
        if not request.user.is_authenticated:
            return HPUploadStatus.NOT_STARTED
        return models.get_upload_status_for_user(request.user)
