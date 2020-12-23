import { createIssuesRouteInfo } from "../issues/routes";
import { createJustfixCrossSiteVisitorRoutes } from "../justfix-cross-site-visitor-routes";
import { createOnboardingRouteInfo } from "../onboarding/routes";
import { createHtmlEmailStaticPageRouteInfo } from "../static-page/routes";
import { ROUTE_PREFIX } from "../util/route-util";

export type HPActionInfo = ReturnType<typeof createHPActionRouteInfo>;

export function createEmergencyHPActionRouteInfo(prefix: string) {
  return {
    [ROUTE_PREFIX]: prefix,
    latestStep: prefix,
    preOnboarding: `${prefix}/splash`,
    splash: `${prefix}/splash`,
    onboarding: createOnboardingRouteInfo(`${prefix}/onboarding`),
    postOnboarding: prefix,
    welcome: `${prefix}/welcome`,
    ...createJustfixCrossSiteVisitorRoutes(prefix),
    sue: `${prefix}/sue`,
    issues: `${prefix}/issues`,
    tenantChildren: `${prefix}/children`,
    accessForInspection: `${prefix}/access`,
    prevAttempts: `${prefix}/previous-attempts`,
    prevAttempts311Modal: `${prefix}/previous-attempts/311-modal`,
    harassmentApartment: `${prefix}/harassment/apartment`,
    harassmentAllegations1: `${prefix}/harassment/allegations/1`,
    harassmentAllegations2: `${prefix}/harassment/allegations/2`,
    harassmentExplain: `${prefix}/harassment/explain`,
    harassmentCaseHistory: `${prefix}/harassment/case-history`,
    yourLandlord: `${prefix}/your-landlord`,
    yourLandlordOptionalDetails: `${prefix}/your-landlord/optional`,
    prepare: `${prefix}/prepare`,
    waitForUpload: `${prefix}/wait`,
    reviewForms: `${prefix}/review`,
    reviewFormsSignModal: `${prefix}/review/sign-modal`,
    verifyEmail: `${prefix}/verify-email`,
    confirmation: `${prefix}/confirmation`,
    serviceInstructionsEmail: createHtmlEmailStaticPageRouteInfo(
      `${prefix}/service-instructions-email`
    ),
    exampleServiceInstructionsEmailForm: `${prefix}/service-instructions-email/example`,
    exampleServiceInstructionsEmail: createHtmlEmailStaticPageRouteInfo(
      `${prefix}/service-instructions-email/example`
    ),
    serviceInstructionsWebpage: `${prefix}/service-instructions`,
  };
}

export function createHPActionRouteInfo(prefix: string) {
  return {
    [ROUTE_PREFIX]: prefix,
    latestStep: prefix,
    preOnboarding: `${prefix}/splash`,
    splash: `${prefix}/splash`,
    onboarding: createOnboardingRouteInfo(`${prefix}/onboarding`),
    postOnboarding: prefix,
    welcome: `${prefix}/welcome`,
    ...createJustfixCrossSiteVisitorRoutes(prefix),
    sue: `${prefix}/sue`,
    issues: createIssuesRouteInfo(`${prefix}/issues`),
    tenantChildren: `${prefix}/children`,
    accessForInspection: `${prefix}/access`,
    prevAttempts: `${prefix}/previous-attempts`,
    prevAttempts311Modal: `${prefix}/previous-attempts/311-modal`,
    urgentAndDangerous: `${prefix}/urgency`,
    harassmentApartment: `${prefix}/harassment/apartment`,
    harassmentAllegations1: `${prefix}/harassment/allegations/1`,
    harassmentAllegations2: `${prefix}/harassment/allegations/2`,
    harassmentExplain: `${prefix}/harassment/explain`,
    harassmentCaseHistory: `${prefix}/harassment/case-history`,
    feeWaiverStart: `${prefix}/fee-waiver`,
    feeWaiverMisc: `${prefix}/fee-waiver/misc`,
    feeWaiverIncome: `${prefix}/fee-waiver/income`,
    feeWaiverExpenses: `${prefix}/fee-waiver/expenses`,
    feeWaiverPublicAssistance: `${prefix}/fee-waiver/public-assistance`,
    yourLandlord: `${prefix}/your-landlord`,
    ready: `${prefix}/ready`,
    waitForUpload: `${prefix}/wait`,
    confirmation: `${prefix}/confirmation`,
  };
}
