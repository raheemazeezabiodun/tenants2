import React, { useContext } from "react";
import Page from "../../ui/page";
import { MiddleProgressStep } from "../../progress/progress-step-route";
import { LetterPreview } from "../../static-page/letter-preview";
import { NorentRoutes } from "../routes";
import { NextButton, BackButton } from "../../ui/buttons";
import { OutboundLink } from "../../analytics/google-analytics";
import { SessionUpdatingFormSubmitter } from "../../forms/session-updating-form-submitter";
import { NorentSendLetterMutation } from "../../queries/NorentSendLetterMutation";
import { Route, Link } from "react-router-dom";
import { Modal, BackOrUpOneDirLevel } from "../../ui/modal";
import { AppContext } from "../../app-context";
import { NorentLetterEmailForUser } from "../letter-content";

const SendLetterModal: React.FC<{
  nextStep: string;
}> = ({ nextStep }) => {
  return (
    <Modal
      title="Shall we send your letter?"
      onCloseGoTo={BackOrUpOneDirLevel}
      withHeading
      render={(ctx) => (
        <>
          <p>
            After this step, you cannot go back to make changes. But don’t
            worry, we’ll explain what to do next.
          </p>
          <SessionUpdatingFormSubmitter
            mutation={NorentSendLetterMutation}
            initialState={{}}
            onSuccessRedirect={nextStep}
          >
            {(sessionCtx) => (
              <div className="buttons jf-two-buttons">
                <Link
                  {...ctx.getLinkCloseProps()}
                  className="jf-is-back-button button is-medium"
                >
                  No
                </Link>
                <NextButton isLoading={sessionCtx.isLoading} label="Yes" />
              </div>
            )}
          </SessionUpdatingFormSubmitter>
        </>
      )}
    />
  );
};

export const NorentLetterPreviewPage = MiddleProgressStep((props) => {
  const { letterContent } = NorentRoutes.locale;
  const { session } = useContext(AppContext);
  const showLetterPreview =
    session.norentScaffolding?.hasLandlordMailingAddress;
  const showEmailPreview = session.norentScaffolding?.hasLandlordEmailAddress;
  return (
    <Page title="Almost there!" withHeading="big" className="content">
      <p>
        Before you send your letter, let's review what will be sent to make sure
        all the information is correct.
      </p>
      {showLetterPreview && (
        <>
          <p>Here's a preview of the letter.</p>
          <LetterPreview
            title="Preview of your NoRent.org letter"
            src={letterContent.html}
          />
          <p>
            You can also{" "}
            <OutboundLink href={letterContent.pdf} target="_blank">
              view this letter as a PDF
            </OutboundLink>
            .
          </p>
        </>
      )}
      {showEmailPreview && (
        <>
          <p>Here’s a preview of the email that will be sent on your behalf:</p>
          <article className="message">
            <div className="message-body has-background-grey-lighter has-text-left has-text-weight-light">
              <NorentLetterEmailForUser />
            </div>
          </article>
        </>
      )}
      <p>Make sure all the information above is correct.</p>
      <div className="buttons jf-two-buttons">
        <BackButton to={props.prevStep} />
        <Link
          to={NorentRoutes.locale.letter.previewSendConfirmModal}
          className="button is-primary is-medium jf-is-next-button"
        >
          Send letter
        </Link>
      </div>
      <Route
        path={NorentRoutes.locale.letter.previewSendConfirmModal}
        exact
        render={() => <SendLetterModal nextStep={props.nextStep} />}
      />
    </Page>
  );
});
