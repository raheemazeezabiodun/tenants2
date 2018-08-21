import pytest

from users.tests.factories import UserFactory
from project.util import schema_json
from project.views import FRONTEND_QUERY_DIR


def get_frontend_queries(*filenames):
    return '\n'.join([
        (FRONTEND_QUERY_DIR / filename).read_text()
        for filename in filenames
    ])


@pytest.mark.django_db
def test_login_works(graphql_client):
    user = UserFactory(phone_number='5551234567', password='blarg')
    result = graphql_client.execute(
        get_frontend_queries(
            'LoginMutation.graphql', 'AllSessionInfo.graphql'),
        variable_values={
            'input': {
                'phoneNumber': '5551234567',
                'password': 'blarg'
            }
        }
    )

    login = result['data']['login']
    assert login['errors'] == []
    assert len(login['session']['csrfToken']) > 0
    assert graphql_client.request.user.pk == user.pk


@pytest.mark.django_db
def test_logout_works(graphql_client):
    user = UserFactory()
    graphql_client.request.user = user
    logout_mutation = get_frontend_queries(
        'LogoutMutation.graphql', 'AllSessionInfo.graphql')
    result = graphql_client.execute(logout_mutation)
    assert len(result['data']['logout']['session']['csrfToken']) > 0
    assert graphql_client.request.user.pk is None


def test_schema_json_is_up_to_date():
    err_msg = (
        f'{schema_json.FILENAME} is out of date! '
        f'Please run "{schema_json.REBUILD_CMDLINE}" to rebuild it.'
    )

    if not schema_json.is_up_to_date():
        raise Exception(err_msg)
