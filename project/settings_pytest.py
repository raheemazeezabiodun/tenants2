from . import justfix_environment  # noqa

justfix_environment.IS_RUNNING_TESTS = True

from .settings import *  # noqa

# Disable legacy auth by default, tests will need
# to override settings if they want to enable it.
LEGACY_MONGODB_URL = ''

# We don't want any actual network requests to go out
# while we're testing, so just point this at a
# nonexistent localhost port.
GEOCODING_SEARCH_URL = "http://127.0.0.1:9999/v1/search"

# Use very fast but horribly insecure password hashing
# to make tests run faster.
PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.MD5PasswordHasher',
)
