import React from "react";
import { USStateChoice } from "../../../../common-data/us-state-choices";
import { Trans } from "@lingui/macro";
import { LocalizedOutboundLinkProps } from "../../ui/localized-outbound-link";

export type StateLocalizedResources = Partial<
  {
    [k in USStateChoice]: LocalizedOutboundLinkProps[];
  }
>;

export const STATE_LOCALIZED_RESOURCES: StateLocalizedResources = {
  CA: [
    {
      children: <Trans>COVID-19 Tenant Relief Act Extension</Trans>,
      hrefs: {
        en: "https://www.bcsh.ca.gov/covidrelief/",
      },
    },
    {
      children: (
        <Trans>
          Apply for Rental Assistance. Qualifying renters are eligible for 100%
          of rent and utilities owed.
        </Trans>
      ),
      hrefs: {
        en: "https://housing.ca.gov/covid_rr/index.html",
        es: "https://housing.ca.gov/covid_rr/index_esp.html",
      },
    },
  ],
  NY: [
    {
      children: <Trans>Eviction Moratorium updates</Trans>,
      hrefs: {
        en:
          "https://www.righttocounselnyc.org/ny_eviction_moratorium_faq?utm_campaign=we_are_powerful&utm_medium=email&utm_source=righttocounselnyc",
        es:
          "https://docs.google.com/document/d/1uzT1lduZAzNLpy_WxSOU1oSOTOPs0YrWekzLd8o6tAs/edit",
      },
    },
    {
      children: <Trans>Cancel Rent Campaign</Trans>,
      hrefs: {
        // Yes, both of these URLs are the same: the english and spanish versions are on the same page.
        en:
          "https://actionnetwork.org/petitions/reclaim-our-homes-rent-suspension-now?source=direct_link&referrer=group-right-to-counsel-nyc-coalition",
        es:
          "https://actionnetwork.org/petitions/reclaim-our-homes-rent-suspension-now?source=direct_link&referrer=group-right-to-counsel-nyc-coalition",
      },
    },
    {
      children: <Trans>Rent Strike Organizing</Trans>,
      hrefs: {
        en:
          "https://d3n8a8pro7vhmx.cloudfront.net/righttocounselnyc/pages/100/attachments/original/1585739362/RTCNYC.COVID19.4.pdf?1585739362",
        es:
          "https://d3n8a8pro7vhmx.cloudfront.net/righttocounselnyc/pages/100/attachments/original/1586436761/Huelga_de_Renta_.pdf?1586436761",
      },
    },
  ],
};
