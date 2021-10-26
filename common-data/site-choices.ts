// This file was auto-generated by commondatabuilder.
// Please don't edit it.

export type SiteChoice = "JUSTFIX"|"NORENT"|"EVICTIONFREE"|"LALETTERBUILDER";

export const SiteChoices: SiteChoice[] = [
  "JUSTFIX",
  "NORENT",
  "EVICTIONFREE",
  "LALETTERBUILDER"
];

const SiteChoiceSet: Set<String> = new Set(SiteChoices);

export function isSiteChoice(choice: string): choice is SiteChoice {
  return SiteChoiceSet.has(choice);
}
