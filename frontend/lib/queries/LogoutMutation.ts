// This file was automatically generated and should not be edited.

import fetchGraphQL from '../fetch-graphql'


/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: LogoutMutation
// ====================================================

export interface LogoutMutation_logout {
  ok: boolean;
  csrfToken: string;
}

export interface LogoutMutation {
  logout: LogoutMutation_logout;
}

/* tslint:disable */
// This file was automatically generated and should not be edited.

//==============================================================
// START Enums and Input Objects
//==============================================================

//==============================================================
// END Enums and Input Objects
//==============================================================
export function fetchLogoutMutation(): Promise<LogoutMutation> {
  // The following query was taken from LogoutMutation.graphql.
  return fetchGraphQL(`mutation LogoutMutation {
    logout {
        ok,
        csrfToken
    }
}
`);
}