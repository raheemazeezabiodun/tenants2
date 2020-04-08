from unittest.mock import patch
import pytest
from django.contrib.auth.hashers import is_password_usable

from project.tests.util import get_frontend_query
from users.models import JustfixUser
from onboarding.schema import session_key_for_step
from .factories import OnboardingInfoFactory


VALID_STEP_DATA = {
    1: {
        'firstName': 'boop',
        'lastName': 'jones',
        'address': '123 boop way',
        'borough': 'MANHATTAN',
        'aptNumber': '3B'
    },
    2: {
        'isInEviction': False,
        'needsRepairs': True,
        'hasNoServices': False,
        'hasPests': False,
        'hasCalled311': False
    },
    3: {
        'leaseType': 'MARKET_RATE',
        'receivesPublicAssistance': 'False'
    },
    '4Version2': {
        'phoneNumber': '5551234567',
        'canWeSms': True,
        'email': 'boop@jones.com',
        'signupIntent': 'LOC',
        'password': 'blarg1234',
        'confirmPassword': 'blarg1234',
        'agreeToTerms': True
    }
}

ONBOARDING_INFO_QUERY = '''
query {
    session {
        onboardingInfo {
            signupIntent
            hasCalled311
        }
    }
}
'''


def _get_step_1_info(graphql_client):
    return graphql_client.execute(
        'query { session { onboardingStep1 { aptNumber, addressVerified } } }'
    )['data']['session']['onboardingStep1']


def _exec_onboarding_step_n(n, graphql_client, **input_kwargs):
    return graphql_client.execute(
        get_frontend_query(f'OnboardingStep{n}Mutation.graphql'),
        variables={'input': {
            **VALID_STEP_DATA[n],
            **input_kwargs
        }}
    )['data'][f'output']


def test_onboarding_step_1_validates_data(graphql_client):
    ob = _exec_onboarding_step_n(1, graphql_client, firstName='')
    assert len(ob['errors']) > 0
    assert session_key_for_step(1) not in graphql_client.request.session
    assert _get_step_1_info(graphql_client) is None


def test_onboarding_step_1_works(graphql_client):
    ob = _exec_onboarding_step_n(1, graphql_client)
    assert ob['errors'] == []
    assert ob['session']['onboardingStep1'] == VALID_STEP_DATA[1]
    assert graphql_client.request.session[session_key_for_step(1)]['apt_number'] == '3B'
    assert _get_step_1_info(graphql_client)['aptNumber'] == '3B'
    assert _get_step_1_info(graphql_client)['addressVerified'] is False


@pytest.mark.django_db
def test_onboarding_step_4_returns_err_if_prev_steps_not_completed(graphql_client):
    result = _exec_onboarding_step_n('4Version2', graphql_client)
    assert result['errors'] == [{
        'field': '__all__',
        'extendedMessages': [
            {"message": "You haven't completed all the previous steps yet.", "code": None}
        ]
    }]


def execute_onboarding(graphql_client, step_data=VALID_STEP_DATA):
    for i in step_data.keys():
        result = _exec_onboarding_step_n(i, graphql_client, **step_data[i])
        assert result['errors'] == []
    return result


@pytest.mark.django_db
def test_onboarding_works(graphql_client, smsoutbox, mailoutbox):
    result = execute_onboarding(graphql_client)

    for i in [1, 2, 3]:
        assert result['session'][f'onboardingStep{i}'] is None
    assert result['session']['phoneNumber'] == '5551234567'

    request = graphql_client.request
    user = JustfixUser.objects.get(phone_number='5551234567')
    oi = user.onboarding_info
    assert user.full_name == 'boop jones'
    assert user.email == 'boop@jones.com'
    assert user.pk == request.user.pk
    assert is_password_usable(user.password) is True
    assert oi.address == '123 boop way'
    assert oi.needs_repairs is True
    assert oi.lease_type == 'MARKET_RATE'
    assert len(smsoutbox) == 1
    assert smsoutbox[0].to == "+15551234567"
    assert "Welcome to JustFix.nyc, boop" in smsoutbox[0].body
    assert len(mailoutbox) == 1
    assert "verify your email" in mailoutbox[0].subject


@pytest.mark.django_db
def test_onboarding_without_optional_steps_works(graphql_client):
    steps = {**VALID_STEP_DATA}
    del steps[2]

    result = execute_onboarding(graphql_client, step_data=steps)

    for i in [1, 3]:
        assert result['session'][f'onboardingStep{i}'] is None
    assert result['session']['phoneNumber'] == '5551234567'

    user = JustfixUser.objects.get(phone_number='5551234567')
    oi = user.onboarding_info
    assert user.full_name == 'boop jones'
    assert oi.needs_repairs is None
    assert oi.lease_type == 'MARKET_RATE'


@pytest.mark.django_db
def test_onboarding_info_is_none_when_it_does_not_exist(graphql_client):
    result = graphql_client.execute(ONBOARDING_INFO_QUERY)['data']['session']
    assert result['onboardingInfo'] is None


@pytest.mark.django_db
def test_onboarding_info_is_present_when_it_exists(graphql_client):
    execute_onboarding(graphql_client)
    result = graphql_client.execute(ONBOARDING_INFO_QUERY)['data']['session']
    assert result['onboardingInfo']['signupIntent'] == 'LOC'


@pytest.mark.django_db
def test_has_called_311_works(graphql_client):
    def query():
        result = graphql_client.execute(ONBOARDING_INFO_QUERY)['data']['session']
        return result['onboardingInfo']['hasCalled311']

    onb = OnboardingInfoFactory(has_called_311=None)
    graphql_client.request.user = onb.user
    assert query() is None

    onb.has_called_311 = True
    onb.save()
    assert query() is True


def test_onboarding_session_info_is_fault_tolerant(graphql_client):
    key = session_key_for_step(1)
    graphql_client.request.session[key] = {'lol': 1}

    with patch('project.util.django_graphql_session_forms.logger') as m:
        assert _get_step_1_info(graphql_client) is None
        m.exception.assert_called_once_with(f'Error deserializing {key} from session')
        assert key not in graphql_client.request.session
