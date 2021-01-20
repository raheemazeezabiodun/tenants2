import React from "react";
import Page from "../../ui/page";
import { ProgressButtons } from "../../ui/buttons";
import { SessionUpdatingFormSubmitter } from "../../forms/session-updating-form-submitter";
import { CheckboxFormField, TextualFormField } from "../../forms/form-fields";
import { ModalLink } from "../../ui/modal";
import { EvictionFreeRoutes } from "../route-info";
import { PrivacyInfoModal } from "../../ui/privacy-info-modal";
import { trackSignup } from "../../analytics/track-signup";
import { OnboardingInfoSignupIntent } from "../../queries/globalTypes";
import { EvictionFreeOnboardingStep } from "./step-decorators";
import { Trans, t } from "@lingui/macro";
import { li18n } from "../../i18n-lingui";
import {
  BlankEvictionFreeCreateAccountInput,
  EvictionFreeCreateAccountMutation,
} from "../../queries/EvictionFreeCreateAccountMutation";

export const EvictionFreeCreateAccount = EvictionFreeOnboardingStep((props) => {
  return (
    <Page title={li18n._(t`Set up an account`)} withHeading="big">
      <div className="content">
        <p>
          Let’s set you up with an account. An account will enable you to save
          your information, download your declaration, and more.
        </p>
      </div>
      <SessionUpdatingFormSubmitter
        mutation={EvictionFreeCreateAccountMutation}
        initialState={{
          ...BlankEvictionFreeCreateAccountInput,
          canWeSms: true,
        }}
        onSuccess={() => trackSignup(OnboardingInfoSignupIntent.EVICTIONFREE)}
        onSuccessRedirect={props.nextStep}
      >
        {(ctx) => (
          <>
            <TextualFormField
              label={li18n._(t`Password`)}
              type="password"
              {...ctx.fieldPropsFor("password")}
            />
            <TextualFormField
              label={li18n._(t`Confirm password`)}
              type="password"
              {...ctx.fieldPropsFor("confirmPassword")}
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
                  EvictionFreeRoutes.locale.declaration.createAccountTermsModal
                }
                render={() => <PrivacyInfoModal />}
              >
                EvictionFree.org terms and conditions
              </ModalLink>
              .
            </CheckboxFormField>
            <ProgressButtons isLoading={ctx.isLoading} back={props.prevStep} />
          </>
        )}
      </SessionUpdatingFormSubmitter>
    </Page>
  );
});