import React from 'react';

import Routes from "./routes";
import Page from "./page";
import { CenteredPrimaryButtonLink, BackButton, NextButton } from './buttons';
import { IssuesRoutes } from './pages/issue-pages';
import { withAppContext, AppContextType } from './app-context';
import { AllSessionInfo_landlordDetails } from './queries/AllSessionInfo';
import { SessionUpdatingFormSubmitter, FormSubmitterChildren } from './forms';
import { GenerateHPActionPDFMutation } from './queries/GenerateHPActionPDFMutation';
import { PdfLink } from './pdf-link';
import { ProgressRoutesProps, buildProgressRoutesComponent } from './progress-routes';
import { OutboundLink } from './google-analytics';
import { HPUploadStatus } from './queries/globalTypes';
import { GetHPActionUploadStatus } from './queries/GetHPActionUploadStatus';
import { Redirect } from 'react-router';
import { SessionPoller } from './session-poller';

const onboardingForHPActionRoute = Routes.hp.onboarding.latestStep;

function HPActionSplash(): JSX.Element {
  return (
    <Page title="Sue your landlord for repairs through an HP Action proceeding" className="content">
      <h1>Sue your landlord for repairs through an HP Action proceeding</h1>
      <p>Welcome to JustFix.nyc! This website will guide you through the process of starting an <strong>HP Action</strong> proceeding.</p>
      <p>An <strong>HP Action</strong> is a legal case you can bring against your landlord for failing to make repairs, not providing essential services, or harassing you.</p>
      <p><em>This service is free, secure, and confidential.</em></p>
      <CenteredPrimaryButtonLink className="is-large" to={onboardingForHPActionRoute}>
        Start my case
      </CenteredPrimaryButtonLink>
    </Page>
  );
}

const HPActionWelcome = withAppContext((props: AppContextType) => {
  const title = `Welcome, ${props.session.firstName}! Let's start your HP Action paperwork.`;

  return (
    <Page title={title}>
      <div className="content">
        <h1>{title}</h1>
        <p>
          An <strong>HP (Housing Part) Action</strong> is a legal case you can bring against your landlord for failing to make repairs, not providing essential services, or harassing you. Here is how it works:
        </p>
        <ol className="has-text-left">
          <li>Answer a few questions about your housing situation.</li>
          <li>We provide you with a pre-filled packet of all the paperwork you’ll need.</li>
          <li><strong>Print out this packet and bring it to Housing Court.</strong> It will include instructions for <strong>filing in court</strong> and <strong>serving your landlord</strong>.
</li>
        </ol>
        <CenteredPrimaryButtonLink to={Routes.hp.issues.home}>
          Select repair issues
        </CenteredPrimaryButtonLink>
        <br/>
        <p>
          <strong>You do not need a lawyer to be successful in an HP Action.</strong> You must be able to show the court that repairs are needed and what those repairs are. This includes photo evidence of the issues, HPD inspection reports, and communication with your landlord.
        </p>
      </div>
    </Page>
  );
});

const HPActionIssuesRoutes = () => (
  <IssuesRoutes
    routes={Routes.hp.issues}
    toBack={Routes.hp.postOnboarding}
    toNext={Routes.hp.yourLandlord}
  />
);

const LandlordDetails = (props: { details: AllSessionInfo_landlordDetails }) => (
  <>
    <p>This is your landlord’s information as registered with the <b>NYC Department of Housing and Preservation (HPD)</b>. This may be different than where you send your rent checks.</p>
    <dl>
      <dt>Name</dt>
      <dd>{props.details.name}</dd>
      <dt>Address</dt>
      <dd>{props.details.address}</dd>
    </dl>
    <p>We'll use these details to automatically fill out your HP Action forms!</p>
  </>
);

const GeneratePDFForm = (props: { children: FormSubmitterChildren<{}> }) => (
  <SessionUpdatingFormSubmitter mutation={GenerateHPActionPDFMutation} initialState={{}}
   onSuccessRedirect={Routes.hp.waitForUpload} {...props} />
);

const HPActionYourLandlord = withAppContext((props: AppContextType) => {
  const details = props.session.landlordDetails;

  return (
    <Page title="Your landlord" className="content">
      <h1 className="title is-4">Your landlord</h1>
      {details && details.isLookedUp && details.name && details.address
        ? <LandlordDetails details={details} />
        : <p>We were unable to retrieve information from the <b>NYC Department of Housing and Preservation (HPD)</b> about your landlord, so you will need to fill out the information yourself once we give you the forms.</p>}
      <GeneratePDFForm>
        {(ctx) =>
          <div className="buttons jf-two-buttons">
            <BackButton to={Routes.hp.issues.home} label="Back" />
            <NextButton isLoading={ctx.isLoading} label="Generate forms"/>
          </div>
        }
      </GeneratePDFForm>
    </Page>
  );
});

const HPActionUploadError = () => (
  <Page title="Alas." className="content">
    <h1>Alas.</h1>
    <p>Unfortunately, an error occurred when generating your HP Action packet.</p>
    <GeneratePDFForm>
      {(ctx) => <NextButton isLoading={ctx.isLoading} label="Try again"/>}
    </GeneratePDFForm>
  </Page>
);

const HPActionWaitForUpload = () => (
  <Page title="Please wait">
    <p className="has-text-centered">
      Please wait while your HP action documents are generated&hellip;
    </p>
    <SessionPoller query={GetHPActionUploadStatus} />
    <section className="section" aria-hidden="true">
      <div className="jf-loading-overlay">
        <div className="jf-loader"/>
      </div>
    </section>
  </Page>
);

const ShowHPUploadStatus = withAppContext((props: AppContextType) => {
  let status = props.session.hpActionUploadStatus;

  switch (status) {
    case HPUploadStatus.STARTED:
    return <HPActionWaitForUpload />;

    case HPUploadStatus.SUCCEEDED:
    return <Redirect to={Routes.hp.confirmation} />;

    case HPUploadStatus.ERRORED:
    return <HPActionUploadError />;

    case HPUploadStatus.NOT_STARTED:
    return <Redirect to={Routes.hp.latestStep} />;
  }
});

const HPActionConfirmation = withAppContext((props: AppContextType) => {
  const href = props.session.latestHpActionPdfUrl;

  return (
    <Page title="Your HP Action packet has been created!!" className="content">
      <h1 className="title is-4">Your HP Action packet has been created!</h1>
      <p>Here is all of your HP Action paperwork, including instructions:</p>
      {href && <PdfLink href={href} label="Download HP Action packet" />}
      <h2>What happens next?</h2>
      <ol>
        <li><strong>Print out this packet and bring it to Housing Court.</strong> Do not sign any of the documents until you bring them to court.</li>
        <li>Once you arrive at court, <strong>go to the clerk’s office to file these papers</strong>. They will assign you an Index Number and various dates.</li>
        <li>After you file your papers, you will need to <strong>serve your landlord and/or management company</strong>. This paperwork is also included in your packet.</li>
      </ol>
      <h2>Want to read more about your rights?</h2>
      <ul>
        <li><OutboundLink href="http://housingcourtanswers.org/answers/for-tenants/hp-actions-tenants/" target="_blank">Housing Court Answers</OutboundLink></li>
        <li><OutboundLink href="https://www.lawhelpny.org/nyc-housing-repairs" target="_blank">LawHelpNY</OutboundLink></li>
        <li><OutboundLink href="http://metcouncilonhousing.org/help_and_answers/how_to_get_repairs" target="_blank">Met Council on Housing</OutboundLink>
          {' '}(<OutboundLink href="http://metcouncilonhousing.org/help_and_answers/how_to_get_repairs_spanish" target="_blank">en español</OutboundLink>)</li>
      </ul>
    </Page>
  );
});

export const HPActionProgressRoutesProps: ProgressRoutesProps = {
  toLatestStep: Routes.hp.latestStep,
  label: "HP Action",
  welcomeSteps: [{
    path: Routes.hp.splash, exact: true, component: HPActionSplash,
    isComplete: (s) => !!s.phoneNumber
  }, {
    path: Routes.hp.welcome, exact: true, component: HPActionWelcome
  }],
  stepsToFillOut: [
    { path: Routes.hp.issues.prefix, component: HPActionIssuesRoutes },
    { path: Routes.hp.yourLandlord, exact: true, component: HPActionYourLandlord,
      isComplete: (s) => s.hpActionUploadStatus !== HPUploadStatus.NOT_STARTED },
  ],
  confirmationSteps: [
    { path: Routes.hp.waitForUpload, exact: true, component: ShowHPUploadStatus,
      isComplete: (s) => s.hpActionUploadStatus === HPUploadStatus.SUCCEEDED },
    { path: Routes.hp.confirmation, exact: true, component: HPActionConfirmation}
  ]
};

const HPActionRoutes = buildProgressRoutesComponent(HPActionProgressRoutesProps);

export default HPActionRoutes;
