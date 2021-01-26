import React from "react";
import { FooterLanguageToggle } from "../../ui/language-toggle";
import { LegalDisclaimer } from "../../ui/legal-disclaimer";

export const EvictionFreeFooter: React.FC<{}> = () => (
  <footer>
    <div className="container has-background-dark">
      <div className="columns">
        <div className="column is-8">
          <div className="content is-size-7">
            <FooterLanguageToggle />
            <LegalDisclaimer website="EvictionFreeNY.org" />
          </div>
        </div>
      </div>
    </div>
  </footer>
);
