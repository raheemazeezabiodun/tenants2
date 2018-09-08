import React from 'react';
import { AllSessionInfo } from './queries/AllSessionInfo';
import Routes from './routes';
import { Redirect, Switch, Route } from 'react-router';
import { LocationDescriptor } from 'history';
import OnboardingStep1 from './pages/onboarding-step-1';
import { GraphQLFetch } from './graphql-client';
import OnboardingStep2 from './pages/onboarding-step-2';
import OnboardingStep3 from './pages/onboarding-step-3';
import OnboardingStep4 from './pages/onboarding-step-4';
import { ProgressBar } from './progress-bar';


export function getLatestOnboardingStep(session: AllSessionInfo): LocationDescriptor {
  let target = Routes.onboarding.step1;

  if (session.onboardingStep1) {
    target = Routes.onboarding.step2
  }

  if (session.onboardingStep2) {
    target = Routes.onboarding.step3;
  }

  if (session.onboardingStep3) {
    target = Routes.onboarding.step4;
  }

  return target;
}

export function RedirectToLatestOnboardingStep(props: { session: AllSessionInfo }): JSX.Element {
  return <Redirect to={getLatestOnboardingStep(props.session)} />
}

export interface OnboardingRoutesProps {
  session: AllSessionInfo;
  fetch: GraphQLFetch;
  onCancelOnboarding: () => void;
  onSessionChange: (session: Partial<AllSessionInfo>) => void;
}

const PROGRESS_PCT = {
  [Routes.onboarding.step1]: 25,
  [Routes.onboarding.step2]: 50,
  [Routes.onboarding.step3]: 75,
  [Routes.onboarding.step4]: 100,
};

function OnboardingProgressBar(): JSX.Element {
  return (
    <Route render={(ctx) => {
      const baseRoute = ctx.location.pathname.slice(0, Routes.onboarding.step1.length);
      const pct = PROGRESS_PCT[baseRoute];
      return typeof(pct) === 'number' && (
        <ProgressBar pct={pct}>
          Onboarding is {pct}% complete.
        </ProgressBar>
      );
    }} />
  );
}

export default function OnboardingRoutes(props: OnboardingRoutesProps): JSX.Element {
  return (
    <div>
      <OnboardingProgressBar />
      <Switch>
        <Route path={Routes.onboarding.latestStep} exact>
          <RedirectToLatestOnboardingStep session={props.session} />
        </Route>
        <Route path={Routes.onboarding.step1}>
          <OnboardingStep1
            onCancel={props.onCancelOnboarding}
            fetch={props.fetch}
            onSuccess={props.onSessionChange}
            initialState={props.session.onboardingStep1}
          />
        </Route>
        <Route path={Routes.onboarding.step2}>
          <OnboardingStep2
            fetch={props.fetch}
            onSuccess={props.onSessionChange}
            initialState={props.session.onboardingStep2}
          />
        </Route>
        <Route path={Routes.onboarding.step3}>
          <OnboardingStep3
            fetch={props.fetch}
            onSuccess={props.onSessionChange}
            initialState={props.session.onboardingStep3}
          />
        </Route>
        <Route path={Routes.onboarding.step4}>
          <OnboardingStep4
            fetch={props.fetch}
            onSuccess={props.onSessionChange}
          />
        </Route>
      </Switch>
    </div>
  );
}
