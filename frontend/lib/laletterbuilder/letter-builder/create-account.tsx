import React from "react";
import Page from "../../ui/page";
import { ProgressButtons } from "../../ui/buttons";
import { SessionUpdatingFormSubmitter } from "../../forms/session-updating-form-submitter";
import { CheckboxFormField } from "../../forms/form-fields";
import { ModalLink } from "../../ui/modal";
import { LaLetterBuilderRouteInfo } from "../route-info";
import { PrivacyInfoModal } from "../../ui/privacy-info-modal";
import { trackSignup } from "../../analytics/track-signup";
import { OnboardingInfoSignupIntent } from "../../queries/globalTypes";
import { LaLetterBuilderOnboardingStep } from "./step-decorators";
import { Trans, t } from "@lingui/macro";
import { li18n } from "../../i18n-lingui";
import {
  BlankLaLetterBuilderCreateAccountInput,
  LaLetterBuilderCreateAccountMutation,
} from "../../queries/LaLetterBuilderCreateAccountMutation";
import { CreatePasswordFields } from "../../common-steps/create-password";

export const LaLetterBuilderCreateAccount = LaLetterBuilderOnboardingStep(
  (props) => {
    return (
      <Page title={li18n._(t`Set up an account`)} withHeading="big">
        <div className="content">
          <p>
            Let’s set you up with an account. An account will enable you to save
            your information, download your declaration, and more.
          </p>
        </div>
        <SessionUpdatingFormSubmitter
          mutation={LaLetterBuilderCreateAccountMutation}
          initialState={{
            ...BlankLaLetterBuilderCreateAccountInput,
            canWeSms: true,
          }}
          onSuccess={() =>
            trackSignup(OnboardingInfoSignupIntent.LALETTERBUILDER)
          }
          onSuccessRedirect={props.nextStep}
        >
          {(ctx) => (
            <>
              <CreatePasswordFields
                passwordProps={ctx.fieldPropsFor("password")}
                confirmPasswordProps={ctx.fieldPropsFor("confirmPassword")}
              />
              <CheckboxFormField {...ctx.fieldPropsFor("canWeSms")}>
                <Trans>
                  Yes, JustFix.nyc can text me to follow up about my housing
                  issues.
                </Trans>
              </CheckboxFormField>
              <CheckboxFormField {...ctx.fieldPropsFor("agreeToTerms")}>
                I agree to the{" "}
                <ModalLink
                  to={
                    LaLetterBuilderRouteInfo.locale.letter
                      .createAccountTermsModal
                  }
                  render={() => <PrivacyInfoModal />}
                >
                  LaLetterBuilder.org terms and conditions
                </ModalLink>
                .
              </CheckboxFormField>
              <ProgressButtons
                isLoading={ctx.isLoading}
                back={props.prevStep}
              />
            </>
          )}
        </SessionUpdatingFormSubmitter>
      </Page>
    );
  }
);
