from typing import Optional
import re
from django.contrib.sites.models import Site
from django.http import HttpRequest
from django.conf import settings
from django.urls import reverse

from ..common_data import Choices


SITE_CHOICES = Choices.from_file("site-choices.json")


def get_default_site() -> Site:
    '''
    Returns the default Site object, as specified by settings.DEFAULT_SITE_ID.
    '''

    return Site.objects._get_site_by_id(settings.DEFAULT_SITE_ID)


def get_site_from_request_or_default(request: Optional[HttpRequest] = None) -> Site:
    '''
    Attempts to retrieve the Site object for the given request. If no request is
    passed, or if no Site maps to it, the default site is returned.
    '''

    if request is None:
        return get_default_site()
    try:
        return Site.objects.get_current(request)
    except Site.DoesNotExist:
        return get_default_site()


def get_site_type(site: Site) -> str:
    if re.match(r'.*norent.*', site.name, re.IGNORECASE):
        return SITE_CHOICES.NORENT
    return SITE_CHOICES.JUSTFIX


def absolutify_url(url: str, request: Optional[HttpRequest] = None) -> str:
    '''
    If the URL is an absolute path, returns the URL prefixed with
    the appropriate Site's protocol and host information.

    If the given URL is already absolute, returns the URL unchanged.
    '''

    if url.startswith('http://') or url.startswith('https://'):
        return url

    if not url.startswith('/'):
        raise ValueError(f"url must be an absolute path: {url}")

    protocol = 'http' if settings.DEBUG else 'https'
    host = get_site_from_request_or_default(request).domain
    return f"{protocol}://{host}{url}"


def absolute_reverse(*args, request: Optional[HttpRequest] = None, **kwargs) -> str:
    '''
    Like Django's reverse(), but ensures the URL includes protocol
    and host information for the appropriate Site, so that it can be
    embedded in an external location, e.g. an email.
    '''

    return absolutify_url(reverse(*args, **kwargs), request=request)


def get_canonical_url(request: HttpRequest):
    '''
    Get the canonical URL for the given request, using the appropriate
    Site's configuration.
    '''

    return absolutify_url(request.get_full_path(), request)


def get_site_base_name(site_type: str) -> str:
    '''
    Returns the base site name given the type of site we are,
    without any additional deployment information.
    '''

    if site_type == SITE_CHOICES.JUSTFIX:
        return "JustFix.nyc"
    elif site_type == SITE_CHOICES.NORENT:
        return "NoRent"
    raise ValueError(f"Invalid site type: {site_type}")


def get_site_name(site_type: str = SITE_CHOICES.JUSTFIX) -> str:
    '''
    Returns the site name. Note that this doesn't actually look at
    Django's current Site object, but rather assumes that we're
    either JustFix.nyc or NoRent and appends any optional
    deployment information to it, to ensure that people don't
    confuse it with production.
    '''

    words = [get_site_base_name(site_type)]

    if settings.NAVBAR_LABEL:
        words.append(settings.NAVBAR_LABEL)

    return ' '.join(words)
