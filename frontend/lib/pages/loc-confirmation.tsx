import React from 'react';

import { withAppContext, AppContextType } from '../app-context';
import { LetterRequestMailChoice } from '../queries/globalTypes';
import { AllSessionInfo_letterRequest } from '../queries/AllSessionInfo';
import Page from '../page';
import { friendlyDate } from '../util';
import { OutboundLink } from '../google-analytics';
import { PdfLink } from '../pdf-link';
import { ProgressiveLoadableConfetti } from '../confetti-loadable';
import { EmailAttachmentForm } from '../email-attachment';
import { EmailLetterMutation } from '../queries/EmailLetterMutation';
import { BigList } from '../big-list';
import { USPS_TRACKING_URL_PREFIX } from "../../../common-data/loc.json";

const DownloadLetterLink = (props: { locPdfURL: string }) => (
  <PdfLink href={props.locPdfURL} label="Download letter" />
);

const getCommonMailNextSteps = () => [
  <li>Once received, your landlord should contact you to schedule time to make repairs for the access dates you provided.</li>,
  <li>While you wait, you should <strong>document your issues with photos</strong> and <strong>call 311 to request an HPD inspection.</strong></li>
];

const getCommonWeMailNextSteps = () => [
  ...getCommonMailNextSteps(),
  <li>We will continue to follow up with you via text message. If your landlord does not follow through, you now have better legal standing to sue your landlord. <strong>This is called an HP Action proceeding.</strong></li>
];

function WeMailedLetterStatus(props: {
  letterRequest: AllSessionInfo_letterRequest,
  locPdfURL: string
}): JSX.Element {
  const {letterSentAt, trackingNumber} = props.letterRequest;
  const url = `${USPS_TRACKING_URL_PREFIX}${trackingNumber}`;

  return (
    <>
      <p>We sent your letter of complaint{letterSentAt && <> on <strong>{friendlyDate(new Date(letterSentAt))}</strong></>}!</p>
      <p>Your <b>USPS Certified Mail<sup>&reg;</sup></b> tracking number is <a href={url} target="_blank" rel="noopener, noreferrer">{trackingNumber}</a>.</p>
      <DownloadLetterLink {...props} />
      <h2>What happens next?</h2>
      <BigList children={getCommonWeMailNextSteps()} />
    </>
  );
}

function WeWillMailLetterStatus(props: {
  letterRequest: AllSessionInfo_letterRequest,
  locPdfURL: string
}): JSX.Element {
  const dateStr = friendlyDate(new Date(props.letterRequest.updatedAt));

  return (
    <>
      <p>We've received your request to mail a letter of complaint on <strong>{dateStr}</strong>. We'll text you a link to your <b>USPS Certified Mail<sup>&reg;</sup></b> tracking number once we have it!</p>
      <DownloadLetterLink {...props} />
      <h2>What happens next?</h2>
      <BigList children={[
        <li>We’ll mail your letter via <b>USPS Certified Mail<sup>&reg;</sup></b> and provide a tracking number via text message.</li>,
        ...getCommonWeMailNextSteps(),
      ]}/>
    </>
  );
}

function UserWillMailLetterStatus(props: { locPdfURL: string }): JSX.Element {
  return (
    <>
      <p>Here is a link to a PDF of your saved letter:</p>
      <DownloadLetterLink {...props} />
      <h2>What happens next?</h2>
      <BigList children={[
        <li>Print out your letter and <strong>mail it via Certified Mail</strong> - this allows you to prove that it was sent to your landlord.</li>,
        ...getCommonMailNextSteps(),
      ]}/>
    </>
  );
}

const knowYourRightsList = (
  <ul>
    <li><OutboundLink href="https://www.metcouncilonhousing.org/help-answers/getting-repairs/" target="_blank">Met Council on Housing</OutboundLink>
          {' '}(<OutboundLink href="https://www.metcouncilonhousing.org/help-answers/how-to-get-repairs-spanish/" target="_blank">en español</OutboundLink>)</li>
    <li><OutboundLink href="http://housingcourtanswers.org/glossary/" target="_blank">Housing Court Answers</OutboundLink></li>
  </ul>
);

const LetterConfirmation = withAppContext((props: AppContextType): JSX.Element => {
  const { letterRequest } = props.session;
  const letterStatusProps = { locPdfURL: props.server.locPdfURL };
  let letterConfirmationPageTitle, letterStatus;

  if (letterRequest && letterRequest.trackingNumber) {
    letterConfirmationPageTitle = 'Your Letter of Complaint has been sent!';
    letterStatus = <WeMailedLetterStatus letterRequest={letterRequest} {...letterStatusProps} />;
  } else if (letterRequest && letterRequest.mailChoice === LetterRequestMailChoice.WE_WILL_MAIL) {
    letterConfirmationPageTitle = 'Your Letter of Complaint is being sent!';
    letterStatus = <WeWillMailLetterStatus letterRequest={letterRequest} {...letterStatusProps} />;
  } else {
    letterConfirmationPageTitle = 'Your Letter of Complaint has been created!';
    letterStatus = <UserWillMailLetterStatus {...letterStatusProps} />;
  }

  return (
    <Page title={letterConfirmationPageTitle} withHeading="big" >
      <ProgressiveLoadableConfetti regenerateForSecs={1} />
      <div className="content">
        {letterStatus}
        <h2>Email a copy of your letter to yourself or someone you trust</h2>
        <EmailAttachmentForm mutation={EmailLetterMutation} noun="letter" />
        <h2>Want to read more about your rights?</h2>
        {knowYourRightsList}
      </div>
    </Page>
  );
});

export default LetterConfirmation;
