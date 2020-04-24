import { ROUTE_PREFIX } from "../../util/route-util";
import { createStartAccountOrLoginRouteInfo } from "../start-account-or-login/routes";

export type NorentLetterBuilderRouteInfo = ReturnType<
  typeof createNorentLetterBuilderRouteInfo
>;

export function createNorentLetterBuilderRouteInfo(prefix: string) {
  return {
    [ROUTE_PREFIX]: prefix,
    latestStep: prefix,
    welcome: `${prefix}/welcome`,
    ...createStartAccountOrLoginRouteInfo(prefix),
    name: `${prefix}/name`,
    city: `${prefix}/city`,
    knowYourRights: `${prefix}/kyr`,
    nationalAddress: `${prefix}/address/national`,
    laAddress: `${prefix}/address/los-angeles`,
    nycAddress: `${prefix}/address/nyc`,
    nycAddressConfirmModal: `${prefix}/address/nyc/confirm-address-modal`,
    email: `${prefix}/email`,
    createAccount: `${prefix}/create-account`,
    createAccountTermsModal: `${prefix}/create-account/terms-modal`,
    landlordName: `${prefix}/landlord/name`,
    landlordEmail: `${prefix}/landlord/email`,
    landlordAddress: `${prefix}/landlord/address`,
    preview: `${prefix}/preview`,
    previewSendConfirmModal: `${prefix}/preview/send-confirm-modal`,
    confirmation: `${prefix}/confirmation`,
  };
}
