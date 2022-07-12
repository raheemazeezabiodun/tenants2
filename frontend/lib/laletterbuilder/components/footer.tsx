import { Trans } from "@lingui/macro";
import React from "react";

import { LegalDisclaimer } from "../../ui/legal-disclaimer";
import { LocalizedOutboundLink } from "../../ui/localized-outbound-link";
import { ClickableLogo } from "./clickable-logo";

export const LaLetterBuilderFooter: React.FC<{}> = () => (
  <footer className="has-background-dark">
    <div className="container">
      <div className="content">
        <div className="columns">
          {/* TODO: change this to match our final URL decision */}
          <div className="column is-6">
            <LegalDisclaimer website="LaLetterBuilder.org" />
          </div>
          <div className="column is-6">
            <ClickableLogo
              imageClassName="jf-laletterbuilder-footer-logo"
              imageUrl="justfix-saje-combined-logo"
            />
            <p>
              <Trans>
                JustFix and SAJE are registered 501(c)(3) nonprofit
                organizations.
              </Trans>
            </p>
          </div>
        </div>
        <br />
        <div className="is-divider"></div>
        <span className="is-uppercase">
          <LocalizedOutboundLink
            hrefs={{
              en: "https://www.justfix.nyc/en/privacy-policy",
              es: "https://www.justfix.nyc/es/privacy-policy",
            }}
          >
            <Trans>Privacy Policy</Trans>
          </LocalizedOutboundLink>
        </span>
        <span className="is-pulled-right is-uppercase">
          <LocalizedOutboundLink
            hrefs={{
              en: "https://www.justfix.nyc/en/terms-of-use/",
              es: "https://www.justfix.nyc/es/terms-of-use/",
            }}
          >
            <Trans>Terms of Use</Trans>
          </LocalizedOutboundLink>
        </span>
      </div>
    </div>
  </footer>
);
