import time
import logging
from typing import List, Dict, Any, Optional
from django.http import HttpResponseBadRequest, HttpResponse
from django.utils.safestring import SafeString
from django.utils import translation
from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings
from django.contrib.sites.models import Site
from users.models import JustfixUser
from project.justfix_environment import BASE_DIR
from project.util.lambda_service import LambdaService
from project.util.site_util import (
    get_site_from_request_or_default,
    get_site_type,
    get_site_origin,
)
from project.graphql_static_request import GraphQLStaticRequest

from .graphql import execute_query, get_initial_session
from .lambda_response import GraphQLQueryPrefetchInfo, LambdaResponse
from .legacy_forms import LegacyFormSubmissionError, get_legacy_form_submission

# This is changed by test suites to ensure that
# everything works okay when the server-side renderer fails
# (relatively) gracefully.
TEST_INTERNAL_SERVER_ERROR = False

NS_PER_MS = 1e+6

LAMBDA_SCRIPT = BASE_DIR / 'lambda.js'

logger = logging.getLogger(__name__)

lambda_service: LambdaService

if settings.USE_LAMBDA_HTTP_SERVER:
    from project.util.lambda_http_client import LambdaHttpClient

    lambda_service = LambdaHttpClient(
        'ReactHttp',
        LAMBDA_SCRIPT,
        script_args=['--serve-http'],
        cwd=BASE_DIR,
        restart_on_script_change=settings.DEBUG
    )
else:
    from project.util.lambda_pool import LambdaPool

    lambda_service = LambdaPool(
        'React',
        LAMBDA_SCRIPT,
        cwd=BASE_DIR,
        restart_on_script_change=settings.DEBUG
    )


def run_react_lambda(initial_props, initial_render_time: int = 0) -> LambdaResponse:
    start_time = time.time_ns()
    response = lambda_service.run_handler(initial_props)
    render_time = initial_render_time + int((time.time_ns() - start_time) / NS_PER_MS)

    pf = response['graphQLQueryToPrefetch']
    if pf is not None:
        pf = GraphQLQueryPrefetchInfo(
            graphql=pf['graphQL'],
            input=pf['input']
        )

    lr = LambdaResponse(
        html=SafeString(response['html']),
        is_static_content=response['isStaticContent'],
        http_headers=response['httpHeaders'],
        modal_html=SafeString(response['modalHtml']),
        title_tag=SafeString(response['titleTag']),
        meta_tags=SafeString(response['metaTags']),
        script_tags=SafeString(response['scriptTags']),
        status=response['status'],
        location=response['location'],
        traceback=response['traceback'],
        graphql_query_to_prefetch=pf,
        render_time=render_time
    )

    if lr.status == 500:
        logger.error(lr.traceback)

    if lr.is_static_content:
        lr = lr._replace(html="<!DOCTYPE html>" + lr.html)

    return lr


def run_react_lambda_with_prefetching(initial_props, request) -> LambdaResponse:
    lambda_response = run_react_lambda(initial_props)

    if lambda_response.status == 200 and lambda_response.graphql_query_to_prefetch:
        # The page rendered, but it has a "loading..." message somewhere on it
        # that's waiting for a GraphQL request to complete. Let's pre-fetch that
        # request and re-render the page, so that the user receives it without
        # any such messages (and so the user can see all the content if their
        # JS isn't working).
        pfquery = lambda_response.graphql_query_to_prefetch
        initial_props['server']['prefetchedGraphQLQueryResponse'] = {
            'graphQL': pfquery.graphql,
            'input': pfquery.input,
            'output': execute_query(request, pfquery.graphql, pfquery.input)
        }
        lambda_response = run_react_lambda(
            initial_props,
            initial_render_time=lambda_response.render_time
        )

    return lambda_response


def get_webpack_public_path_url() -> str:
    return f'{settings.STATIC_URL}frontend/'


def render_lambda_static_content(lr: LambdaResponse):
    ctype = lr.http_headers.get('Content-Type')
    if ctype is None:
        res = HttpResponse(lr.html, status=lr.status)
    elif ctype == 'application/pdf':
        from loc.views import pdf_response
        res = pdf_response(lr.html)
    elif ctype == 'text/plain; charset=utf-8':
        from project.util.html_to_text import html_to_text
        res = HttpResponse(
            html_to_text(lr.html).encode("utf-8"),
            status=lr.status
        )
    else:
        raise ValueError(f'Invalid Content-Type from lambda response: {ctype}')

    for key, value in lr.http_headers.items():
        res[key] = value
    return res


def get_enabled_locales() -> List[str]:
    return [
        locale for locale, name in settings.LANGUAGES
    ]


def create_initial_props_for_lambda(
    site: Site,
    url: str,
    locale: str,
    initial_session: Dict[str, Any],
    origin_url: str,
    legacy_form_submission: Optional[Dict[str, Any]] = None
):
    webpack_public_path_url = get_webpack_public_path_url()
    site_type = get_site_type(site)

    # Currently, the schema for this structure needs to be mirrored
    # in the AppProps interface in frontend/lib/app.tsx. So if you
    # add or remove anything here, make sure to do the same over there!
    initial_props: Dict[str, Any] = {
        'initialURL': url,
        'initialSession': initial_session,
        'locale': locale,
        'server': {
            'originURL': origin_url,
            'siteName': site.name,
            'siteType': site_type,
            'staticURL': settings.STATIC_URL,
            'webpackPublicPathURL': webpack_public_path_url,
            'adminIndexURL': reverse('admin:index'),
            'batchGraphQLURL': reverse('batch-graphql'),
            'locHtmlURL': reverse('loc', args=('html',)),
            'locPdfURL': reverse('loc', args=('pdf',)),
            'enableSafeModeURL': reverse('safe_mode:enable'),
            'redirectToLegacyAppURL': reverse('redirect-to-legacy-app'),
            'navbarLabel': settings.NAVBAR_LABEL,
            'wowOrigin': settings.WOW_ORIGIN,
            'efnycOrigin': settings.EFNYC_ORIGIN,
            'enableEmergencyHPAction': settings.ENABLE_EMERGENCY_HP_ACTION,
            'mapboxAccessToken': settings.MAPBOX_ACCESS_TOKEN,
            'isDemoDeployment': settings.IS_DEMO_DEPLOYMENT,
            'enabledLocales': get_enabled_locales(),
            'debug': settings.DEBUG,
            'facebookAppId': settings.FACEBOOK_APP_ID
        },
        'testInternalServerError': TEST_INTERNAL_SERVER_ERROR,
    }

    if legacy_form_submission is not None:
        initial_props['legacyFormSubmission'] = legacy_form_submission

    return initial_props


def create_initial_props_for_lambda_from_request(
    request,
    url: str,
    legacy_form_submission: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    locale = translation.get_language_from_request(request, check_path=True)

    return create_initial_props_for_lambda(
        site=get_site_from_request_or_default(request),
        url=url,
        locale=locale,
        initial_session=get_initial_session(request),
        origin_url=request.build_absolute_uri('/')[:-1],
        legacy_form_submission=legacy_form_submission,
    )


def get_language_from_url_or_default(url: str) -> str:
    return translation.get_language_from_path(url) or settings.LANGUAGE_CODE


def render_raw_lambda_static_content(
    url: str,
    site: Site,
    user: Optional[JustfixUser] = None,
) -> Optional[LambdaResponse]:
    '''
    This function can be used by the server to render static content in the
    lambda service. Normally such content is delivered directly to a user's
    browser, but sometimes we want to access it in the server so we can
    do other things with it, e.g. generate a PDF to send to an API, or
    render an HTML email.
    '''

    request = GraphQLStaticRequest(user=user)
    initial_props = create_initial_props_for_lambda(
        site=site,
        url=url,
        locale=get_language_from_url_or_default(url),
        initial_session=get_initial_session(request),
        origin_url=get_site_origin(site),
    )
    lr = run_react_lambda_with_prefetching(initial_props, request)
    if not (lr.is_static_content and lr.status == 200):
        logger.error(
            "Expected (is_static_content=True, status=200) but got "
            f"(is_static_content={lr.is_static_content}, status={lr.status}) for "
            f"{url}"
        )
        return None
    return lr


def react_rendered_view(request):
    url = request.path
    querystring = request.GET.urlencode()
    if querystring:
        url += f'?{querystring}'

    legacy_form_submission = None

    if request.method == "POST":
        try:
            # It's important that we process the legacy form submission
            # *before* getting the initial session, so that when we
            # get the initial session, it reflects any state changes
            # made by the form submission. This will ensure the same
            # behavior between baseline (non-JS) and progressively
            # enhanced (JS) clients.
            legacy_form_submission = get_legacy_form_submission(request)
        except LegacyFormSubmissionError as e:
            return HttpResponseBadRequest(e.args[0])

    initial_props = create_initial_props_for_lambda_from_request(
        request,
        url=url,
        legacy_form_submission=legacy_form_submission,
    )

    lambda_response = run_react_lambda_with_prefetching(initial_props, request)

    script_tags = lambda_response.script_tags
    if lambda_response.status == 500:
        script_tags = ''
    elif lambda_response.status == 302 and lambda_response.location:
        return redirect(to=lambda_response.location)

    logger.debug(f"Rendering {url} in Node.js took {lambda_response.render_time} ms.")

    if lambda_response.is_static_content:
        return render_lambda_static_content(lambda_response)

    return render(request, 'frontend/index.html', {
        'initial_render': lambda_response.html,
        'locale': initial_props['locale'],
        'enable_analytics': not request.user.is_staff,
        'modal_html': lambda_response.modal_html,
        'title_tag': lambda_response.title_tag,
        'site_type': initial_props['server']['siteType'],
        'meta_tags': lambda_response.meta_tags,
        'script_tags': script_tags,
        'initial_props': initial_props,
    }, status=lambda_response.status)
