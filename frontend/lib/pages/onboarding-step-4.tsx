import React from 'react';
import { OnboardingStep4Input } from "../queries/globalTypes";
import Page from '../page';
import { FormContext, SessionUpdatingFormSubmitter } from '../forms';
import autobind from 'autobind-decorator';
import { OnboardingStep4Mutation } from '../queries/OnboardingStep4Mutation';
import Routes, { getSignupIntentRouteInfo } from '../routes';
import { NextButton, BackButton } from "../buttons";
import { CheckboxFormField, TextualFormField } from '../form-fields';
import { PhoneNumberFormField } from '../phone-number-form-field';
import { ModalLink } from '../modal';
import { PrivacyInfoModal } from './onboarding-step-1';
import { fbq } from '../faceboox-pixel';
import { assertNotNull } from '../util';
import { signupIntentFromOnboardingInfo } from '../signup-intent';

const blankInitialState: OnboardingStep4Input = {
  phoneNumber: '',
  canWeSms: true,
  password: '',
  confirmPassword: '',
  agreeToTerms: false
};

export default class OnboardingStep4 extends React.Component {
  @autobind
  renderForm(ctx: FormContext<OnboardingStep4Input>): JSX.Element {
    return (
      <React.Fragment>
        <PhoneNumberFormField label="Phone number" {...ctx.fieldPropsFor('phoneNumber')} />
        <CheckboxFormField {...ctx.fieldPropsFor('canWeSms')}>
          Yes, JustFix.nyc can text me to follow up about my housing issues.
        </CheckboxFormField>
        <br />
        <TextualFormField label="Create a password (optional)" type="password" {...ctx.fieldPropsFor('password')} />
        <TextualFormField label="Please confirm your password (optional)" type="password" {...ctx.fieldPropsFor('confirmPassword')} />
        <CheckboxFormField {...ctx.fieldPropsFor('agreeToTerms')}>
          I agree to the {" "}
          <ModalLink to={Routes.onboarding.step4TermsModal} component={PrivacyInfoModal}>
            JustFix.nyc terms and conditions
          </ModalLink>.
        </CheckboxFormField>
        <div className="buttons jf-two-buttons">
          <BackButton to={Routes.onboarding.step3} label="Back" />
          <NextButton isLoading={ctx.isLoading} label="Create my account" />
        </div>
      </React.Fragment>
    );
  }

  render() {
    return (
      <Page title="Contact information">
        <div>
          <h1 className="title is-4">Your contact information</h1>
          <SessionUpdatingFormSubmitter
            mutation={OnboardingStep4Mutation}
            initialState={blankInitialState}
            onSuccessRedirect={(output) => (
              getSignupIntentRouteInfo(
                signupIntentFromOnboardingInfo(assertNotNull(output.session).onboardingInfo)
              ).postOnboarding
            )}
            onSuccess={() => fbq('track','CompleteRegistration')}
          >{this.renderForm}</SessionUpdatingFormSubmitter>
        </div>
      </Page>
    );
  }
}
