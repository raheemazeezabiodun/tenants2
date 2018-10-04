import React from 'react';

import Page from "../page";
import { FormContext, SessionUpdatingFormSubmitter } from '../forms';
import { RadiosFormField } from '../form-fields';

import { withAppContext } from '../app-context';
import { NextButton, BackButton } from "../buttons";
import Routes from '../routes';
import { LetterRequestInput, LetterRequestMailChoice } from '../queries/globalTypes';
import { LetterRequestMutation } from '../queries/LetterRequestMutation';
import { DjangoChoices } from '../common-data';
import { exactSubsetOrDefault } from '../util';

const LOC_MAILING_CHOICES = require('../../../common-data/loc-mailing-choices.json') as DjangoChoices;

const DEFAULT_INPUT: LetterRequestInput = {
  mailChoice: LetterRequestMailChoice.WE_WILL_MAIL
};


function renderForm(ctx: FormContext<LetterRequestInput>): JSX.Element {
  return (
    <React.Fragment>
      <RadiosFormField
        label="JustFix.nyc will mail this letter to your landlord via certified mail and will cover the mailing costs for you."
        choices={LOC_MAILING_CHOICES}
        {...ctx.fieldPropsFor('mailChoice') }
      />
      <div className="buttons">
        <BackButton to={Routes.loc.yourLandlord} label="Back" />
        <NextButton isLoading={ctx.isLoading} label="Finish" />
      </div>
    </React.Fragment>
  );
}

const LetterPreview = withAppContext((props) => (
  <div className="box has-text-centered jf-loc-preview">
    <iframe title="Preview of your letter of complaint" src={props.server.locHtmlURL}></iframe>
  </div>
));

export default function LetterRequestPage(): JSX.Element {
  return (
    <Page title="Review the Letter of Complaint">
      <h1 className="title">Review the Letter of Complaint</h1>
      <div className="content">
        <p>Here is a preview of the letter for you to review. It includes the repair issues you selected from the Issue Checklist.</p>
        <LetterPreview />
      </div>
      <SessionUpdatingFormSubmitter
        mutation={LetterRequestMutation}
        initialState={(session) => exactSubsetOrDefault(session.letterRequest, DEFAULT_INPUT)}
        onSuccessRedirect={Routes.loc.confirmation}
      >
        {renderForm}
      </SessionUpdatingFormSubmitter>
    </Page>
  );
}
