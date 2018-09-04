// This file was automatically generated and should not be edited.

import * as AllSessionInfo from './AllSessionInfo'
/* tslint:disable */
// This file was automatically generated and should not be edited.

import { LoginInput } from "./globalTypes";

// ====================================================
// GraphQL mutation operation: LoginMutation
// ====================================================

export interface LoginMutation_login_errors {
  /**
   * The camel-cased name of the input field, or '__all__' for non-field errors.
   */
  field: string;
  /**
   * A list of human-readable validation errors.
   */
  messages: string[];
}

export interface LoginMutation_login_session_onboardingStep1 {
  name: string;
  address: string;
  aptNumber: string;
  borough: string;
}

export interface LoginMutation_login_session_onboardingStep2 {
  /**
   * Has the user received an eviction notice?
   */
  isInEviction: boolean;
  /**
   * Does the user need repairs in their apartment?
   */
  needsRepairs: boolean;
  /**
   * Is the user missing essential services like water?
   */
  hasNoServices: boolean;
  /**
   * Does the user have pests like rodents or bed bugs?
   */
  hasPests: boolean;
  /**
   * Has the user called 311 before?
   */
  hasCalled311: boolean;
}

export interface LoginMutation_login_session_onboardingStep3 {
  leaseType: string;
  /**
   * Does the user receive public assistance, e.g. Section 8?
   */
  receivesPublicAssistance: boolean;
}

export interface LoginMutation_login_session {
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
  onboardingStep1: LoginMutation_login_session_onboardingStep1 | null;
  onboardingStep2: LoginMutation_login_session_onboardingStep2 | null;
  onboardingStep3: LoginMutation_login_session_onboardingStep3 | null;
}

export interface LoginMutation_login {
  /**
   * A list of validation errors in the form, if any. If the form was valid, this list will be empty.
   */
  errors: LoginMutation_login_errors[];
  session: LoginMutation_login_session | null;
}

export interface LoginMutation {
  login: LoginMutation_login;
}

export interface LoginMutationVariables {
  input: LoginInput;
}

export function fetchLoginMutation(fetchGraphQL: (query: string, args?: any) => Promise<any>, args: LoginMutationVariables): Promise<LoginMutation> {
  // The following query was taken from LoginMutation.graphql.
  return fetchGraphQL(`mutation LoginMutation($input: LoginInput!) {
    login(input: $input) {
        errors {
            field,
            messages
        },
        session {
            ...AllSessionInfo
        }
    }
}

${AllSessionInfo.graphQL}`, args);
}