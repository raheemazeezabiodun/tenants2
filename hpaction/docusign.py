from typing import Tuple
import base64
from django.conf import settings

from users.models import JustfixUser
from docusign.core import docusign_client_user_id
import docusign_esign as dse
from .models import HPActionDocuments


# The recipient ID for the tenant in the signing flow. This appears to be a
# number local to a specific signing, rather than a globally unique identifier.
TENANT_RECIPIENT_ID = '1'

# The document ID for the HP Action packet in the signing flow. This appears
# to be a number local to a specific signing, rather than a globally unique
# identifier.
HPA_DOCUMENT_ID = '1'


def create_envelope_definition_for_hpa(docs: HPActionDocuments) -> dse.EnvelopeDefinition:
    '''
    Create a DocuSign envelope definition for the given HP Action documents.
    '''

    user = docs.user
    pdf_bytes = docs.pdf_file.open().read()
    base64_pdf = base64.b64encode(pdf_bytes).decode('ascii')

    document = dse.Document(
        document_base64=base64_pdf,
        name=f"HP Action forms for {user.full_name}",
        file_extension="pdf",
        document_id=HPA_DOCUMENT_ID,
    )

    signer = dse.Signer(
        email=user.email,
        name=user.full_name,
        recipient_id=TENANT_RECIPIENT_ID,
        routing_order="1",
        client_user_id=docusign_client_user_id(user),
    )

    # These coordinates were found by manually creating a DocuSign template based on
    # generated HP Action forms, creating fields using the drag-and-drop UI,
    # and noting their locations.

    sign_here_petition = dse.SignHere(
        document_id=HPA_DOCUMENT_ID,
        page_number='4',
        recipient_id=TENANT_RECIPIENT_ID,
        tab_label='SignHereTab',
        x_position='419',
        y_position='556',
    )

    sign_here_verification = dse.SignHere(
        document_id=HPA_DOCUMENT_ID,
        page_number='4',
        recipient_id=TENANT_RECIPIENT_ID,
        tab_label='SignHereTab',
        x_position='419',
        y_position='667',
    )

    sign_here_hpd_inspection = dse.SignHere(
        document_id=HPA_DOCUMENT_ID,
        page_number='5',
        recipient_id=TENANT_RECIPIENT_ID,
        tab_label='SignHereTab',
        x_position='446',
        y_position='625',
    )

    signer.tabs = dse.Tabs(
        sign_here_tabs=[
            sign_here_petition,
            sign_here_verification,
            sign_here_hpd_inspection
        ],
    )

    user_cc = dse.CarbonCopy(
        email=user.email,
        name=user.full_name,
        recipient_id="2",
        routing_order="2",
    )

    envelope_definition = dse.EnvelopeDefinition(
        email_subject=f"HP Action forms for {user.full_name}",
        documents=[document],
        recipients=dse.Recipients(signers=[signer], carbon_copies=[user_cc]),
        status="sent",
    )

    assert isinstance(envelope_definition, dse.EnvelopeDefinition)

    return envelope_definition


def create_envelope_and_recipient_view_for_hpa(
    user: JustfixUser,
    envelope_definition: dse.EnvelopeDefinition,
    api_client: dse.ApiClient,
    return_url: str,
) -> Tuple[dse.EnvelopeSummary, str]:
    '''
    Create a DocuSign envelope and recipient view request for
    HP Action documents represented by a given envelope definition.

    Returns a tuple containing the envelope summary and the
    URL to redirect the user to.
    '''

    envelope_api = dse.EnvelopesApi(api_client)
    envelope = envelope_api.create_envelope(
        settings.DOCUSIGN_ACCOUNT_ID,
        envelope_definition=envelope_definition
    )

    assert isinstance(envelope, dse.EnvelopeSummary)

    envelope_id = envelope.envelope_id
    recipient_view_request = dse.RecipientViewRequest(
        authentication_method='None',  # TODO: This should probably change?
        client_user_id=docusign_client_user_id(user),
        recipient_id=TENANT_RECIPIENT_ID,
        return_url=return_url,
        user_name=user.full_name,
        email=user.email,
    )

    results = envelope_api.create_recipient_view(
        settings.DOCUSIGN_ACCOUNT_ID,
        envelope_id,
        recipient_view_request=recipient_view_request,
    )

    return (envelope, results.url)
