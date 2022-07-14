// This file was auto-generated by commondatabuilder.
// Please don't edit it.

import { t } from "@lingui/macro";
import { li18n } from '../frontend/lib/i18n-lingui';

export type LaIssueRoomChoice = "BEDROOM"|"LIVING_ROOM"|"DINING_ROOM"|"BATHROOM"|"HALLWAY"|"KITCHEN"|"COMMON_AREAS"|"OTHER"|"BROKEN"|"NOT_ENOUGH"|"WATER"|"GAS"|"ELECTRICITY"|"LAUNDRY_ROOM"|"FRONT_DOOR"|"BACK_DOOR"|"BUILDING_MAIN_ENTRANCE"|"BUILDING_PARKING_ENTRANCE"|"BUILDING_EXIT"|"FLOOR_LEVEL";

export const LaIssueRoomChoices: LaIssueRoomChoice[] = [
  "BEDROOM",
  "LIVING_ROOM",
  "DINING_ROOM",
  "BATHROOM",
  "HALLWAY",
  "KITCHEN",
  "COMMON_AREAS",
  "OTHER",
  "BROKEN",
  "NOT_ENOUGH",
  "WATER",
  "GAS",
  "ELECTRICITY",
  "LAUNDRY_ROOM",
  "FRONT_DOOR",
  "BACK_DOOR",
  "BUILDING_MAIN_ENTRANCE",
  "BUILDING_PARKING_ENTRANCE",
  "BUILDING_EXIT",
  "FLOOR_LEVEL"
];

const LaIssueRoomChoiceSet: Set<String> = new Set(LaIssueRoomChoices);

export function isLaIssueRoomChoice(choice: string): choice is LaIssueRoomChoice {
  return LaIssueRoomChoiceSet.has(choice);
}

export type LaIssueRoomChoiceLabels = {
  [k in LaIssueRoomChoice]: string;
};

export function getLaIssueRoomChoiceLabels(): LaIssueRoomChoiceLabels {
  return {
    BEDROOM: li18n._(t`Bedroom`),
    LIVING_ROOM: li18n._(t`Living room`),
    DINING_ROOM: li18n._(t`Dining room`),
    BATHROOM: li18n._(t`Bathroom`),
    HALLWAY: li18n._(t`Hallway`),
    KITCHEN: li18n._(t`Kitchen`),
    COMMON_AREAS: li18n._(t`Common areas (parking, hallway, etc.)`),
    OTHER: li18n._(t`Other`),
    BROKEN: li18n._(t`Broken`),
    NOT_ENOUGH: li18n._(t`Not enough`),
    WATER: li18n._(t`Water`),
    GAS: li18n._(t`Gas`),
    ELECTRICITY: li18n._(t`Electricity`),
    LAUNDRY_ROOM: li18n._(t`Laundry room`),
    FRONT_DOOR: li18n._(t`Front door`),
    BACK_DOOR: li18n._(t`Back door`),
    BUILDING_MAIN_ENTRANCE: li18n._(t`Building main entrance`),
    BUILDING_PARKING_ENTRANCE: li18n._(t`Building parking entrance`),
    BUILDING_EXIT: li18n._(t`Building exit`),
    FLOOR_LEVEL: li18n._(t`Floor level`),
  };
}
