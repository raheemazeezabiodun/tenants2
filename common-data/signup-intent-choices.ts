// This file was auto-generated by commondatabuilder.
// Please don't edit it.

export type SignupIntent = "LOC"|"HP"|"EHP"|"NORENT"|"EVICTIONFREE"|"LALETTERBUILDER";

export const SignupIntents: SignupIntent[] = [
  "LOC",
  "HP",
  "EHP",
  "NORENT",
  "EVICTIONFREE",
  "LALETTERBUILDER"
];

const SignupIntentSet: Set<String> = new Set(SignupIntents);

export function isSignupIntent(choice: string): choice is SignupIntent {
  return SignupIntentSet.has(choice);
}

export type SignupIntentLabels = {
  [k in SignupIntent]: string;
};

export function getSignupIntentLabels(): SignupIntentLabels {
  return {
    LOC: "Letter of Complaint",
    HP: "HP Action",
    EHP: "Emergency HP Action",
    NORENT: "No rent letter",
    EVICTIONFREE: "Eviction free",
    LALETTERBUILDER: "LA Letter Builder",
  };
}
