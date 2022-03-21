import React from "react";
import { Switch, Route } from "react-router-dom";
import AccessDatesPage from "../../../loc/access-dates";
import {
  ProgressRoutesProps,
  buildProgressRoutesComponent,
} from "../../../progress/progress-routes";
import { skipStepsIf } from "../../../progress/skip-steps-if";
import { createStartAccountOrLoginSteps } from "../../../start-account-or-login/routes";
import { createLetterStaticPageRoutes } from "../../../static-page/routes";
import { isUserLoggedIn } from "../../../util/session-predicates";
import { LaLetterBuilderRouteInfo } from "../../route-info";
import { LaLetterBuilderMyLetters, WelcomeMyLetters } from "../my-letters";
import { LaLetterBuilderCreateAccount } from "../../components/create-account";
import {
  HabitabilityLetterForUserStaticPage,
  HabitabilityLetterEmailToLandlordForUserStaticPage,
  HabitabilitySampleLetterSamplePage,
  HabitabilityLetterEmailToLandlordForUser,
  HabitabilityLetterTranslation,
} from "./habitability-letter-content";
import { createLaLetterBuilderPreviewPage } from "../../components/letter-preview";
import { LaLetterBuilderSendOptions } from "../send-options";
import {
  LaLetterBuilderAskName,
  LaLetterBuilderAskCityState,
  LaLetterBuilderAskNationalAddress,
} from "../../components/useful-components";
import { LaLetterBuilderLandlordNameAddressEmail } from "../../components/landlord-info";
import { LaLetterBuilderRiskConsent } from "../../components/consent";
import { t } from "@lingui/macro";
import { li18n } from "../../../i18n-lingui";
import { LaIssuesRoutes } from "../issues";

const HabitabilityRoutes: React.FC<{}> = () => (
  <Switch>
    {createLetterStaticPageRoutes(
      LaLetterBuilderRouteInfo.locale.habitability.letterContent,
      HabitabilityLetterForUserStaticPage
    )}
    <Route
      path={LaLetterBuilderRouteInfo.locale.habitability.letterEmail}
      exact
      component={HabitabilityLetterEmailToLandlordForUserStaticPage}
    />
    {createLetterStaticPageRoutes(
      LaLetterBuilderRouteInfo.locale.habitability.sampleLetterContent,
      HabitabilitySampleLetterSamplePage
    )}
    <Route component={HabitabilityProgressRoutes} />
  </Switch>
);

export const getHabitabilityProgressRoutesProps = (): ProgressRoutesProps => {
  const routes = LaLetterBuilderRouteInfo.locale.habitability;
  const createAccountOrLoginSteps = [
    ...createStartAccountOrLoginSteps(routes),
    {
      path: routes.name,
      exact: true,
      component: LaLetterBuilderAskName,
    },
    {
      path: routes.city,
      exact: false,
      component: LaLetterBuilderAskCityState,
    },
    {
      path: routes.nationalAddress,
      exact: false,
      // TODO: add something that short circuits if the user isn't in LA
      component: LaLetterBuilderAskNationalAddress,
    },
    {
      path: routes.riskConsent,
      component: LaLetterBuilderRiskConsent,
    },
    {
      path: routes.createAccount,
      component: LaLetterBuilderCreateAccount,
    },
  ];

  return {
    label: li18n._(t`Build your Letter`),
    introProgressSection: {
      label: li18n._(t`Create an Account`),
      num_steps: createAccountOrLoginSteps.length,
    },
    toLatestStep: routes.latestStep,
    welcomeSteps: [
      {
        path: routes.welcome,
        exact: true,
        component: WelcomeMyLetters,
      },
    ],
    stepsToFillOut: [
      ...skipStepsIf(isUserLoggedIn, [...createAccountOrLoginSteps]),
      {
        path: routes.myLetters,
        exact: true,
        component: LaLetterBuilderMyLetters,
      },
      {
        path: routes.issues.prefix,
        component: LaLetterBuilderIssuesRoutes,
      },
      {
        path: routes.landlordInfo,
        exact: false,
        component: LaLetterBuilderLandlordNameAddressEmail,
      },
      {
        path: routes.accessDates,
        exact: true,
        component: AccessDatesPage,
      },
      {
        path: routes.preview,
        exact: true,
        component: HabitabilityPreviewPage,
      },
      {
        path: routes.sending,
        exact: true,
        component: LaLetterBuilderSendOptions,
      },
    ],
    confirmationSteps: [
      {
        path: routes.confirmation,
        exact: true,
        component: LaLetterBuilderMyLetters,
      },
    ],
  };
};

export const HabitabilityProgressRoutes = buildProgressRoutesComponent(
  getHabitabilityProgressRoutesProps
);

const LaLetterBuilderIssuesRoutes = () => (
  <LaIssuesRoutes
    routes={LaLetterBuilderRouteInfo.locale.habitability.issues}
    toBack={LaLetterBuilderRouteInfo.locale.home}
    toNext={LaLetterBuilderRouteInfo.locale.habitability.landlordInfo}
  ></LaIssuesRoutes>
);

const HabitabilityPreviewPage = createLaLetterBuilderPreviewPage(
  LaLetterBuilderRouteInfo.getLocale("en").habitability.letterContent,
  HabitabilityLetterEmailToLandlordForUser,
  HabitabilityLetterTranslation
);

export default HabitabilityRoutes;