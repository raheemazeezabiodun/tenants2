import { Trans } from "@lingui/macro";
import React from "react";

import { LegalDisclaimer } from "../../ui/legal-disclaimer";
import { LocalizedOutboundLink } from "../../ui/localized-outbound-link";
import { StaticImage } from "../../ui/static-image";
import { getLaLetterBuilderImageSrc } from "../homepage";

export const LaLetterBuilderFooter: React.FC<{}> = () => (
  <footer className="has-background-dark">
    <div className="container">
      <div className="columns">
        <div className="column is-8">
          <div className="content">
            <LegalDisclaimer website="LaLetterBuilder.org" />
            <StaticImage
              ratio="is-3by1"
              src={getLaLetterBuilderImageSrc("justfix-saje-combined-logo")}
              alt="JustFix SAJE"
            />
            <p>
              <Trans>
                JustFix and SAJE are registered 501(c)(3) nonprofit
                organizations.
              </Trans>
            </p>
            <br />
            <div className="is-divider"></div>
            <span className="is-uppercase">
              <LocalizedOutboundLink
                // TODO: UPDATE THESE LINKS TO NEW LA LETTER BUILDER SPECIFIC PAGES
                hrefs={{
                  en: "https://www.justfix.nyc/en/privacy-policy-norent",
                  es: "https://www.justfix.nyc/es/privacy-policy-norent",
                }}
              >
                <Trans>Privacy Policy</Trans>
              </LocalizedOutboundLink>
            </span>
            <span className="is-pulled-right is-uppercase">
              <LocalizedOutboundLink
                // TODO: UPDATE THESE LINKS TO NEW LA LETTER BUILDER SPECIFIC PAGES
                hrefs={{
                  en: "https://www.justfix.nyc/en/terms-of-use-norent/",
                  es: "https://www.justfix.nyc/es/terms-of-use-norent/",
                }}
              >
                <Trans>Terms of Use</Trans>
              </LocalizedOutboundLink>
            </span>
          </div>
        </div>
      </div>
    </div>
  </footer>
);
