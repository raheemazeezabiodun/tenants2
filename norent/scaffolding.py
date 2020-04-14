import pydantic


# This should change whenever our scaffolding model's fields change.
VERSION = '1'


class NorentScaffolding(pydantic.BaseModel):
    '''
    This is just some scaffolding we have in place of an actual
    Django Model (or collection of models).  It allows us to get
    off the ground running without having to dedicate ourselves
    to a particular database schema.
    '''

    first_name: str = ''

    last_name: str = ''

    # e.g. "666 FIFTH AVENUE"
    street: str = ''

    city: str = ''

    # e.g. "NY"
    state: str = ''

    zip_code: str = ''

    apt_number: str = ''

    email: str = ''

    phone_number: str = ''

    landlord_name: str = ''

    # e.g. "666 FIFTH AVENUE, APT 2"
    landlord_primary_line: str = ''

    landlord_city: str = ''

    landlord_state: str = ''

    landlord_zip_code: str = ''

    landlord_email: str = ''

    landlord_phone_number: str = ''