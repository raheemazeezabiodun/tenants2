export type StartAccountOrLoginRouteInfo = ReturnType<
  typeof createStartAccountOrLoginRouteInfo
>;

export function createStartAccountOrLoginRouteInfo(prefix: string) {
  return {
    phoneNumber: `${prefix}/phone/ask`,
    phoneNumberTermsModal: `${prefix}/phone/ask/terms-modal`,
    verifyPhoneNumber: `${prefix}/phone/verify`,
    setPassword: `${prefix}/password/set`,
    verifyPassword: `${prefix}/password/verify`,
    forgotPasswordModal: `${prefix}/password/verify/forgot-modal`,
  };
}
