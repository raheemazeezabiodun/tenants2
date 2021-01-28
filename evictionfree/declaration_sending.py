from io import BytesIO
import logging
from django.conf import settings
from django.utils import timezone
from django.http import FileResponse

from evictionfree.models import SubmittedHardshipDeclaration
from users.models import JustfixUser
from project import slack, locales
from frontend.static_content import (
    email_react_rendered_content_with_attachment,
)
from project.util.site_util import SITE_CHOICES
from .housing_court import get_housing_court_info_for_user
from . import hardship_declaration, cover_letter


# The URL, relative to the localized site root, that renders the EvictionFreeNY
# email to the landlord.
EVICTIONFREE_EMAIL_TO_LANDLORD_URL = "declaration-email-to-landlord.html"

# The URL, relative to the localized site root, that renders the EvictionFreeNY
# email to the user.
EVICTIONFREE_EMAIL_TO_USER_URL = "declaration-email-to-user.html"

# The URL, relative to the localized site root, that renders the EvictionFreeNY
# email to the housing court.
EVICTIONFREE_EMAIL_TO_HOUSING_COURT_URL = "declaration-email-to-housing-court.html"


logger = logging.getLogger(__name__)


def declaration_pdf_response(pdf_bytes: bytes) -> FileResponse:
    """
    Creates a FileResponse for the given PDF bytes and an
    appropriate filename for the declaration.
    """

    return FileResponse(BytesIO(pdf_bytes), filename="letter.pdf")


def create_declaration(user: JustfixUser) -> SubmittedHardshipDeclaration:
    hd_vars = hardship_declaration.get_vars_for_user(user)
    assert hd_vars is not None
    cl_vars = cover_letter.get_vars_for_user(user)
    assert cl_vars is not None
    shd = SubmittedHardshipDeclaration(
        user=user,
        locale=user.locale,
        cover_letter_variables=cl_vars.dict(),
        cover_letter_html=cover_letter.render_cover_letter_html(cl_vars),
        declaration_variables=hd_vars.dict(),
    )
    shd.full_clean()
    shd.save()
    return shd


def render_declaration(decl: SubmittedHardshipDeclaration) -> bytes:
    from loc.views import render_pdf_bytes
    from norent.letter_sending import _merge_pdfs

    v = hardship_declaration.HardshipDeclarationVariables(**decl.declaration_variables)
    form_pdf_bytes = hardship_declaration.fill_hardship_pdf(v, decl.locale)
    cover_letter_pdf_bytes = render_pdf_bytes(decl.cover_letter_html)
    pdf_bytes = _merge_pdfs([cover_letter_pdf_bytes, form_pdf_bytes])

    return pdf_bytes


def email_declaration_to_landlord(decl: SubmittedHardshipDeclaration, pdf_bytes: bytes) -> bool:
    if settings.IS_DEMO_DEPLOYMENT:
        logger.info(f"Not emailing {decl} to landlord because this is a demo deployment.")
        return False

    if decl.emailed_at is not None:
        logger.info(f"{decl} has already been emailed to the landlord.")
        return False

    ld = decl.user.landlord_details
    assert ld.email

    email_react_rendered_content_with_attachment(
        SITE_CHOICES.EVICTIONFREE,
        decl.user,
        EVICTIONFREE_EMAIL_TO_LANDLORD_URL,
        is_html_email=True,
        recipients=[ld.email],
        attachment=declaration_pdf_response(pdf_bytes),
        # Force the locale of this email to English, since that's what the
        # landlord will read the email as.
        locale=locales.DEFAULT,
    )

    decl.emailed_at = timezone.now()
    decl.save()

    return True


def send_declaration_via_lob(decl: SubmittedHardshipDeclaration, pdf_bytes: bytes) -> bool:
    """
    Mails the declaration to the user's landlord via Lob. Does
    nothing if it has already been sent.

    Returns True if the declaration was just sent.
    """

    if decl.mailed_at is not None:
        logger.info(f"{decl} has already been mailed to the landlord.")
        return False

    # TODO: Implement this, set response to result of lob_api.mail_certified_letter().

    # TODO: Set letter.lob_letter_object to response.

    # TODO: Set tracking number to response["tracking_number"].
    decl.tracking_number = "123456789"

    decl.mailed_at = timezone.now()
    decl.save()

    # TODO: Send SMS informing user of sending and tracking number.
    return True


def send_declaration_to_housing_court(decl: SubmittedHardshipDeclaration, pdf_bytes: bytes) -> bool:
    if settings.IS_DEMO_DEPLOYMENT:
        logger.info(f"Not emailing {decl} to housing court because this is a demo deployment.")
        return False

    if decl.emailed_to_housing_court_at is not None:
        logger.info(f"{decl} has already been sent to the housing court.")
        return False

    user = decl.user

    hci = get_housing_court_info_for_user(user)

    if not hci:
        logger.info(f"{decl} has no housing court info, so we can't send it to one.")
        return False

    # TODO: We should set the sender to something other than noreply, so we
    # can see/process replies from housing court.
    email_react_rendered_content_with_attachment(
        SITE_CHOICES.EVICTIONFREE,
        decl.user,
        EVICTIONFREE_EMAIL_TO_HOUSING_COURT_URL,
        is_html_email=True,
        recipients=[hci.email],
        attachment=declaration_pdf_response(pdf_bytes),
        # Force the locale of this email to English, since that's what the
        # housing court person will read the email as.
        locale=locales.DEFAULT,
    )

    decl.emailed_to_housing_court_at = timezone.now()
    decl.save()

    return True


def send_declaration_to_user(decl: SubmittedHardshipDeclaration, pdf_bytes: bytes) -> bool:
    if decl.emailed_to_user_at is not None:
        logger.info(f"{decl} has already been sent to the user.")
        return False

    user = decl.user
    assert user.email

    email_react_rendered_content_with_attachment(
        SITE_CHOICES.EVICTIONFREE,
        user,
        EVICTIONFREE_EMAIL_TO_USER_URL,
        is_html_email=True,
        recipients=[user.email],
        attachment=declaration_pdf_response(pdf_bytes),
        # Use the user's preferred locale, since they will be the one
        # reading it.
        locale=user.locale,
    )

    decl.emailed_to_user_at = timezone.now()
    decl.save()

    return True


def send_declaration(decl: SubmittedHardshipDeclaration):
    """
    Send the given declaration using whatever information is populated
    in the user's landlord details: that is, if we have the landlord's
    email, then send an email of the declaration, and if we have
    the landlord's mailing address, then send a physical copy
    of the declaration.

    This will also send a copy of the declaration to the user's
    housing court, and to the user themselves.

    If any part of the sending fails, this function can be called
    again and it won't send multiple copies of the declaration.
    """

    pdf_bytes = render_declaration(decl)
    user = decl.user
    ld = user.landlord_details

    if ld.email:
        email_declaration_to_landlord(decl, pdf_bytes)

    if ld.address_lines_for_mailing:
        send_declaration_via_lob(decl, pdf_bytes)

    send_declaration_to_housing_court(decl, pdf_bytes)

    if user.email:
        send_declaration_to_user(decl, pdf_bytes)

    slack.sendmsg_async(
        f"{slack.hyperlink(text=user.first_name, href=user.admin_url)} "
        f"has sent a hardship declaration!",
        is_safe=True,
    )


def create_and_send_declaration(user: JustfixUser):
    """
    Create a SubmittedHardshipDeclaration model and send it.
    """

    decl = create_declaration(user)
    send_declaration(decl)
