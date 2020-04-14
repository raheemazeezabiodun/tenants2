import React from "react";
import Page from "../ui/page";
import { SessionUpdatingFormSubmitter } from "../forms/session-updating-form-submitter";
import { TextualFormField } from "../forms/form-fields";
import { exactSubsetOrDefault, assertNotNull } from "../util/util";
import { NorentRoutes } from "./routes";
import { USStateFormField } from "../forms/mailing-address-fields";
import { ProgressButtons } from "../ui/buttons";
import {
  NorentLandlordInfoMutation,
  BlankNorentLandlordInfoInput,
} from "../queries/NorentLandlordInfoMutation";
import { PhoneNumberFormField } from "../forms/phone-number-form-field";
import { ProgressStepProps } from "../progress/progress-step-route";

export const NorentLandlordInfoPage: React.FC<ProgressStepProps> = (props) => {
  return (
    <Page
      title="Your landlord or management company's information"
      withHeading="big"
      className="content"
    >
      <p>
        We'll use this information to email and mail a letter to your landlord
        or management company.
      </p>
      <SessionUpdatingFormSubmitter
        mutation={NorentLandlordInfoMutation}
        initialState={(s) =>
          exactSubsetOrDefault(
            s.norentScaffolding,
            BlankNorentLandlordInfoInput
          )
        }
        onSuccessRedirect={NorentRoutes.locale.home}
      >
        {(ctx) => (
          <>
            <TextualFormField
              {...ctx.fieldPropsFor("landlordName")}
              label="Landlord/management company's name"
            />
            <TextualFormField
              {...ctx.fieldPropsFor("landlordPrimaryLine")}
              label="Address"
            />
            <TextualFormField
              {...ctx.fieldPropsFor("landlordCity")}
              label="City"
            />
            <USStateFormField {...ctx.fieldPropsFor("landlordState")} />
            <TextualFormField
              {...ctx.fieldPropsFor("landlordZipCode")}
              label="Zip code"
            />
            <TextualFormField
              type="email"
              {...ctx.fieldPropsFor("landlordEmail")}
              label="Email address (highly recommended)"
            />
            <PhoneNumberFormField
              {...ctx.fieldPropsFor("landlordPhoneNumber")}
              label="Phone number"
            />
            <ProgressButtons
              isLoading={ctx.isLoading}
              back={assertNotNull(props.prevStep)}
            />
          </>
        )}
      </SessionUpdatingFormSubmitter>
    </Page>
  );
};