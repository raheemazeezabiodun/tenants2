// This file was auto-generated by commondatabuilder.
// Please don't edit it.

import { t } from "@lingui/macro";
import { li18n } from '../frontend/lib/i18n-lingui';

export type LetterChoice = "HABITABILITY"|"CA_HARASSMENT"|"LA_HARASSMENT"|"PRIVACY";

export const LetterChoices: LetterChoice[] = [
  "HABITABILITY",
  "CA_HARASSMENT",
  "LA_HARASSMENT",
  "PRIVACY"
];

const LetterChoiceSet: Set<String> = new Set(LetterChoices);

export function isLetterChoice(choice: string): choice is LetterChoice {
  return LetterChoiceSet.has(choice);
}

export type LetterChoiceLabels = {
  [k in LetterChoice]: string;
};

export function getLetterChoiceLabels(): LetterChoiceLabels {
  return {
    HABITABILITY: li18n._(t`Habitability (CA)`),
    CA_HARASSMENT: li18n._(t`Harassment (CA)`),
    LA_HARASSMENT: li18n._(t`Harassment (LA City/TAHO)`),
    PRIVACY: li18n._(t`Right to Privacy (CA)`),
  };
}