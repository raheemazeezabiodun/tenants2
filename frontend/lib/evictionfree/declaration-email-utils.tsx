import { AllSessionInfo } from "../queries/AllSessionInfo";
import { friendlyUTCDate } from "../util/date-util";

export type EvictionFreeDeclarationEmailProps = {
  firstName: string;
  fullName: string;
  landlordName: string;
  dateSubmitted: string;
  trackingNumber: string;
  indexNumber: string;
  wasEmailedToHousingCourt: boolean;
  wasEmailedToLandlord: boolean;
  wasMailedToLandlord: boolean;
};

export function sessionToEvictionFreeDeclarationEmailProps(
  s: AllSessionInfo
): EvictionFreeDeclarationEmailProps | null {
  const shd = s.submittedHardshipDeclaration;
  const ld = s.landlordDetails;

  if (!(shd && s.firstName && ld && ld.name)) return null;

  const hdd = s.hardshipDeclarationDetails;

  return {
    firstName: s.firstName,
    fullName: `${s.firstName} ${s.lastName}`,
    landlordName: ld.name,
    dateSubmitted: friendlyUTCDate(shd.createdAt),
    indexNumber: hdd?.indexNumber ?? "",
    trackingNumber: shd.trackingNumber,
    wasEmailedToHousingCourt: !!shd.emailedToHousingCourtAt,
    wasEmailedToLandlord: !!shd.emailedAt,
    wasMailedToLandlord: !!shd.mailedAt,
  };
}

export function evictionFreeDeclarationEmailFormalSubject(
  options: EvictionFreeDeclarationEmailProps
): string {
  const parts = ["Hardship Declaration", options.fullName];

  if (options.indexNumber) {
    parts.push(`Index #: ${options.indexNumber}`);
  }

  parts.push(`submitted ${options.dateSubmitted}`);

  return parts.join(" - ");
}