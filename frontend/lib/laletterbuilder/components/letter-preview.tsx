import { t, Trans } from "@lingui/macro";
import React, { useContext } from "react";
import { AppContext } from "../../app-context";
import { li18n } from "../../i18n-lingui";
import { MiddleProgressStep } from "../../progress/progress-step-route";
import { AllSessionInfo } from "../../queries/AllSessionInfo";
import { LetterPreview } from "../../static-page/letter-preview";
import { ProgressButtonsAsLinks } from "../../ui/buttons";
import {
  ForeignLanguageOnly,
  InYourLanguageTranslation,
} from "../../ui/cross-language";
import { OutboundLink } from "../../ui/outbound-link";
import Page from "../../ui/page";

const Microcopy: React.FC<{ children: React.ReactNode }> = (props) => (
  <p className="is-uppercase is-size-7">{props.children}</p>
);

const InYourLanguageMicrocopy: React.FC<{
  additionalContent?: JSX.Element;
}> = (props) => (
  <Microcopy>
    <InYourLanguageTranslation />
    {props.additionalContent && <> {props.additionalContent}</>}
  </Microcopy>
);

type LetterContent = {
  html: string;
  pdf: string;
};

type LetterPreviewProps = {
  title: string;
  letterContent: LetterContent;
  emailContent: React.FC;
  letterTranslation: React.FC;
  session: AllSessionInfo;
  prevStep: string;
  nextStep: string;
};

const LetterPreviewPage: React.FC<LetterPreviewProps> = (props) => {
  const isMailingLetter = props.session.landlordDetails?.address;
  const isEmailingLetter = props.session.landlordDetails?.email;
  const LetterTranslation = props.letterTranslation;
  const EmailContent = props.emailContent;
  return (
    <Page
      title={li18n._(t`Review your letter`)}
      withHeading="big"
      className="content"
    >
      <p>
        <Trans>
          Before you send your letter, let's review what will be sent to make
          sure all the information is correct.
        </Trans>
      </p>
      <>
        <p>
          {isEmailingLetter && !isMailingLetter ? (
            <Trans>
              Here's a preview of the letter that will be attached in an email
              to your landlord:
            </Trans>
          ) : (
            <Trans>Here's a preview of the letter:</Trans>
          )}
        </p>
        <ForeignLanguageOnly>
          <InYourLanguageMicrocopy />
          <LetterTranslation />
          <Microcopy>
            <Trans>English version</Trans>
          </Microcopy>
        </ForeignLanguageOnly>
        <LetterPreview
          title={li18n._(t`Preview of your letter`)}
          src={props.letterContent.html}
        />
        <p>
          <OutboundLink href={props.letterContent.pdf} target="_blank">
            <Trans>View this letter as a PDF</Trans>
          </OutboundLink>
        </p>
        {isMailingLetter && (
          <p>
            <Trans>
              We will be mailing this letter on your behalf by USPS certified
              mail and will be providing a tracking number.
            </Trans>
          </p>
        )}
      </>
      <br />
      {isEmailingLetter && (
        <>
          <p>
            <Trans>
              Here’s a preview of the email that will be sent on your behalf:
            </Trans>
          </p>
          <br />
          <ForeignLanguageOnly>
            <InYourLanguageMicrocopy
              additionalContent={
                <Trans>(Note: the email will be sent in English)</Trans>
              }
            />
          </ForeignLanguageOnly>
          <article className="message">
            <div className="message-header has-text-weight-normal">
              <Trans>To:</Trans> {props.session.landlordDetails?.name}{" "}
              {props.session.landlordDetails?.email &&
                `<${props.session.landlordDetails?.email}>`}
            </div>
            <div className="message-body has-text-left">
              <EmailContent />
            </div>
          </article>
        </>
      )}
      <p>
        <Trans>Make sure all the information above is correct.</Trans>
      </p>
      <ProgressButtonsAsLinks back={props.prevStep} next={props.nextStep} />
    </Page>
  );
};

export function createLaLetterBuilderPreviewPage(
  englishVersionOfLetterContent: LetterContent,
  emailContent: React.FC<{}>,
  letterTranslation: React.FC<{}>
) {
  return MiddleProgressStep((props) => {
    const { session } = useContext(AppContext);

    return (
      <LetterPreviewPage
        title="LA Letter builder title"
        letterContent={englishVersionOfLetterContent}
        emailContent={emailContent}
        letterTranslation={letterTranslation}
        session={session}
        prevStep={props.prevStep}
        nextStep={props.nextStep}
      />
    );
  });
}