import React, { useContext } from "react";
import Page from "../../ui/page";
import { AppContext } from "../../app-context";
import { OutboundLink } from "../../analytics/google-analytics";
import {
  getUSStateChoiceLabels,
  USStateChoice,
} from "../../../../common-data/us-state-choices";
import { LetterBuilderAccordion } from "./welcome";

const checkCircleSvg = require("../../svg/check-circle-solid.svg") as JSX.Element;

const NORENT_FEEDBACK_FORM_URL = "https://airtable.com/shrrnQD3kXUQv1xm3";
const CANCEL_RENT_PETITION_URL = "https://cancelrent.us/";

export const NorentConfirmation: React.FC<{}> = () => {
  const { session } = useContext(AppContext);
  const letter = session.norentLatestLetter;
  const user = session.norentScaffolding;
  const stateName =
    user?.state && getUSStateChoiceLabels()[user?.state as USStateChoice];

  return (
    <Page title="You've sent your letter" className="content">
      <div className="media">
        <div className="media-left">
          <i className="has-text-info">{checkCircleSvg}</i>
        </div>
        <div className="media-content">
          <h2 className="title">You've sent your letter</h2>
        </div>
      </div>
      <p>
        Your letter has been sent to your landlord via email. A copy of your
        letter has also been sent to your email.
      </p>
      {letter?.trackingNumber && (
        <p className="is-size-4 has-text-weight-bold">
          Tracking #: {letter?.trackingNumber}.
        </p>
      )}
      <br />
      <h2 className="title is-spaced has-text-info">What happens next?</h2>
      <h3 className="title jf-alt-title-font">Gather documentation</h3>
      <p>
        While you wait for your landlord to respond, gather as much
        documentation as you can. This can include a letter from your employer,
        receipts, doctor’s notes etc.
      </p>
      {stateName && (
        <>
          <p>
            {stateName} has specific documentation requirements to support your
            letter to your landlord.
          </p>
          <LetterBuilderAccordion question="Find out more">
            <article className="message">
              <div className="message-body has-background-grey-lighter has-text-left">
                <p>
                  In {stateName}, you have 7 days to send documentation to your
                  landlord proving you can’t pay rent.
                </p>
                <p>Some types of documentation you can gather include:</p>
                <ul>
                  <li>
                    <h4 className="title jf-alt-title-font">
                      Childcare expense receipts
                    </h4>
                    <p>
                      Lorem ipsum dolor sit amet, consectetur adipiscing elit.
                      Mauris quis fringilla nulla.
                    </p>
                  </li>
                  <li>
                    <h4 className="title jf-alt-title-font">
                      Letter from your employer
                    </h4>
                    <p>
                      Lorem ipsum dolor sit amet, consectetur adipiscing elit.
                      Mauris quis fringilla nulla.
                    </p>
                  </li>
                  <li>
                    <h4 className="title jf-alt-title-font">
                      Exercise your rights
                    </h4>
                    <p>
                      Lorem ipsum dolor sit amet, consectetur adipiscing elit.
                      Mauris quis fringilla nulla.
                    </p>
                  </li>
                </ul>
              </div>
            </article>
          </LetterBuilderAccordion>
        </>
      )}
      <h3 className="title jf-alt-title-font">
        Contact a lawyer if your landlord retaliates
      </h3>
      <p>
        It’s possible that your landlord will retaliate once they’ve received
        your letter. This is illegal. Contact your local legal aid provider for
        assistance.
      </p>
      <h3 className="title jf-alt-title-font">Build power in numbers</h3>
      <p>
        Our homes, health, and collective safety and futures are on the line.
        Millions of us don’t know how we are going to pay our rent, mortgage, or
        utilities on May 1st, yet landlords and banks are expecting payment as
        if it’s business as usual. It’s not.
      </p>
      <p>
        Join millions of us to fight for a future free from debt and to win a
        national suspension on rent, mortgage and utility payments!
      </p>
      <br />
      <p className="has-text-centered">
        <OutboundLink
          className="button is-primary is-large jf-is-extra-wide"
          href={CANCEL_RENT_PETITION_URL}
          target="_blank"
          rel="noopener noreferrer"
        >
          Sign the petition
        </OutboundLink>
      </p>
      <h3 className="title jf-alt-title-font">Give us feedback</h3>
      <p>
        This tool is provided by JustFix.nyc. We’re a non-profit that creates
        tools for tenants and the housing rights movement. We always want
        feedback to improve our tools.
      </p>
      <br />
      <p className="has-text-centered">
        <OutboundLink
          className="button is-primary is-large jf-is-extra-wide"
          href={NORENT_FEEDBACK_FORM_URL}
          target="_blank"
          rel="noopener noreferrer"
        >
          Give feedback
        </OutboundLink>
      </p>
    </Page>
  );
};
