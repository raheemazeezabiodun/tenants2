// This file was automatically generated and should not be edited.

import * as AllSessionInfo from './AllSessionInfo'
/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: LogoutMutation
// ====================================================

export interface LogoutMutation_logout_session_onboardingStep1 {
  name: string;
  address: string;
  aptNumber: string;
}

export interface LogoutMutation_logout_session {
  /**
   * The phone number of the currently logged-in user, or null if not logged-in.
   */
  phoneNumber: string | null;
  /**
   * The cross-site request forgery (CSRF) token.
   */
  csrfToken: string;
  /**
   * Whether or not the currently logged-in user is a staff member.
   */
  isStaff: boolean;
  onboardingStep1: LogoutMutation_logout_session_onboardingStep1 | null;
}

export interface LogoutMutation_logout {
  session: LogoutMutation_logout_session;
}

export interface LogoutMutation {
  logout: LogoutMutation_logout;
}

export function fetchLogoutMutation(fetchGraphQL: (query: string, args?: any) => Promise<any>, ): Promise<LogoutMutation> {
  // The following query was taken from LogoutMutation.graphql.
  return fetchGraphQL(`mutation LogoutMutation {
    logout {
        session {
            ...AllSessionInfo
        }
    }
}

${AllSessionInfo.graphQL}`);
}