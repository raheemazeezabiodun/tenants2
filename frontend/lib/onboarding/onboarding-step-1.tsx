import React, { useContext } from "react";
import Page from "../ui/page";
import { OnboardingRouteInfo } from "../routes";
import { Link, Route, RouteComponentProps, withRouter } from "react-router-dom";
import { SessionUpdatingFormSubmitter } from "../forms/session-updating-form-submitter";
import {
  OnboardingStep1Input,
  OnboardingInfoSignupIntent,
} from "../queries/globalTypes";
import autobind from "autobind-decorator";
import {
  OnboardingStep1Mutation,
  BlankOnboardingStep1Input,
} from "../queries/OnboardingStep1Mutation";
import { assertNotNull, exactSubsetOrDefault } from "../util/util";
import { Modal, BackOrUpOneDirLevel } from "../ui/modal";
import {
  TextualFormField,
  renderSimpleLabel,
  LabelRenderer,
} from "../forms/form-fields";
import { NextButton } from "../ui/buttons";
import { withAppContext, AppContextType, AppContext } from "../app-context";
import { OutboundLink } from "../analytics/google-analytics";
import { FormContext } from "../forms/form-context";
import { AddressAndBoroughField } from "../forms/address-and-borough-form-field";
import {
  ConfirmAddressModal,
  redirectToAddressConfirmationOrNextStep,
} from "../ui/address-confirmation";
import { ClearSessionButton } from "../forms/clear-session-button";
import { updateAddressFromBrowserStorage } from "../browser-storage";
import { getSignupIntentLabels } from "../../../common-data/signup-intent-choices";

function createAddressLabeler(toStep1AddressModal: string): LabelRenderer {
  return (label, labelProps) => (
    <div className="level is-marginless is-mobile">
      <div className="level-left">
        <div className="level-item is-marginless">
          {renderSimpleLabel(label, labelProps)}
        </div>
      </div>
      <div className="level-right">
        <div className="level-item is-marginless">
          <Link to={toStep1AddressModal} className="is-size-7">
            Why do you need my address?
          </Link>
        </div>
      </div>
    </div>
  );
}

export function PrivacyInfoModal(): JSX.Element {
  return (
    <Modal
      title="Your privacy is very important to us!"
      onCloseGoTo={BackOrUpOneDirLevel}
      render={(ctx) => (
        <>
          <div className="jf-is-scrollable-if-too-tall">
            <h5>
              Your privacy is very important to us! Here are some important
              things to know:
            </h5>
            <ul>
              <li>Your personal information is secure.</li>
              <li>
                We don’t use your personal information for profit or sell it to
                third parties.
              </li>
              <li>
                We use your address to find information about your landlord and
                your building.
              </li>
            </ul>
            <p>
              Our Privacy Policy enables sharing anonymized data with approved
              tenant advocacy organizations exclusively to help further our
              tenants rights mission. The Privacy Policy contains information
              regarding what data we collect, how we use it, and the choices you
              have regarding your personal information. If you’d like to read{" "}
              more, please review our full{" "}
              <OutboundLink
                href="https://www.justfix.nyc/privacy-policy"
                target="_blank"
              >
                Privacy Policy
              </OutboundLink>{" "}
              and{" "}
              <OutboundLink
                href="https://www.justfix.nyc/terms-of-use"
                target="_blank"
              >
                Terms of Use
              </OutboundLink>
              .
            </p>
          </div>
          <div className="has-text-centered">
            <Link
              className="button is-primary is-medium"
              {...ctx.getLinkCloseProps()}
            >
              Got it!
            </Link>
          </div>
        </>
      )}
    />
  );
}

function Step1ConfirmAddressModal(props: { toStep3: string }): JSX.Element {
  const addrInfo =
    useContext(AppContext).session.onboardingStep1 || BlankOnboardingStep1Input;
  return <ConfirmAddressModal nextStep={props.toStep3} {...addrInfo} />;
}

type OnboardingStep1Props = {
  disableProgressiveEnhancement?: boolean;
  routes: OnboardingRouteInfo;
  toCancel: string;
  signupIntent: OnboardingInfoSignupIntent;
} & RouteComponentProps<any> &
  AppContextType;

class OnboardingStep1WithoutContexts extends React.Component<
  OnboardingStep1Props
> {
  readonly cancelControlRef: React.RefObject<
    HTMLDivElement
  > = React.createRef();
  private readonly renderAddressLabel = createAddressLabeler(
    this.props.routes.step1AddressModal
  );

  renderFormButtons(isLoading: boolean): JSX.Element {
    return (
      <div className="field is-grouped jf-two-buttons">
        <div className="control" ref={this.cancelControlRef} />
        <div className="control">
          <NextButton isLoading={isLoading} />
        </div>
      </div>
    );
  }

  @autobind
  renderForm(ctx: FormContext<OnboardingStep1Input>): JSX.Element {
    const { routes } = this.props;

    return (
      <React.Fragment>
        <div className="columns is-mobile">
          <div className="column">
            <TextualFormField
              label="First name"
              {...ctx.fieldPropsFor("firstName")}
            />
          </div>
          <div className="column">
            <TextualFormField
              label="Last name"
              {...ctx.fieldPropsFor("lastName")}
            />
          </div>
        </div>
        <AddressAndBoroughField
          disableProgressiveEnhancement={
            this.props.disableProgressiveEnhancement
          }
          renderAddressLabel={this.renderAddressLabel}
          addressProps={ctx.fieldPropsFor("address")}
          boroughProps={ctx.fieldPropsFor("borough")}
        />
        <TextualFormField
          label="Apartment number"
          autoComplete="address-line2 street-address"
          {...ctx.fieldPropsFor("aptNumber")}
        />
        <Route
          path={routes.step1AddressModal}
          exact
          component={PrivacyInfoModal}
        />
        <p>
          Your privacy is very important to us! Everything on JustFix.nyc is
          secure.{" "}
          <Link to={routes.step1AddressModal}>
            Click here to learn more
            <span className="jf-sr-only"> about our privacy policy</span>
          </Link>
          .
        </p>
        <br />
        {this.renderFormButtons(ctx.isLoading)}
      </React.Fragment>
    );
  }

  render() {
    const { routes } = this.props;
    const actionLabel = getSignupIntentLabels()[this.props.signupIntent];

    return (
      <Page
        title={`Create an account to get started with your ${actionLabel}!`}
        withHeading
      >
        <div>
          <SessionUpdatingFormSubmitter
            mutation={OnboardingStep1Mutation}
            initialState={(s) =>
              exactSubsetOrDefault(s.onboardingStep1, BlankOnboardingStep1Input)
            }
            updateInitialStateInBrowser={updateAddressFromBrowserStorage}
            onSuccessRedirect={(output, input) =>
              redirectToAddressConfirmationOrNextStep({
                input,
                resolved: assertNotNull(
                  assertNotNull(output.session).onboardingStep1
                ),
                nextStep: routes.step3,
                confirmation: routes.step1ConfirmAddressModal,
              })
            }
          >
            {this.renderForm}
          </SessionUpdatingFormSubmitter>
        </div>

        <ClearSessionButton
          to={this.props.toCancel}
          portalRef={this.cancelControlRef}
          disableProgressiveEnhancement={
            this.props.disableProgressiveEnhancement
          }
          label="Cancel"
        />
        <Route
          path={routes.step1ConfirmAddressModal}
          exact
          render={() => <Step1ConfirmAddressModal toStep3={routes.step3} />}
        />
      </Page>
    );
  }
}

const OnboardingStep1 = withAppContext(
  withRouter(OnboardingStep1WithoutContexts)
);

export default OnboardingStep1;