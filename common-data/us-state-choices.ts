// This file was auto-generated by commondatabuilder.
// Please don't edit it.

export type USStateChoice = "AK"|"AL"|"AS"|"AZ"|"AR"|"CA"|"CO"|"CT"|"DE"|"DC"|"FL"|"GA"|"GU"|"HI"|"ID"|"IL"|"IN"|"IA"|"KS"|"KY"|"LA"|"ME"|"MD"|"MA"|"MI"|"MN"|"MP"|"MS"|"MO"|"MT"|"NE"|"NV"|"NH"|"NJ"|"NM"|"NY"|"NC"|"ND"|"OH"|"OK"|"OR"|"PA"|"PR"|"RI"|"SC"|"SD"|"TN"|"TX"|"UT"|"VT"|"VA"|"VI"|"WA"|"WV"|"WI"|"WY";

export const USStateChoices: USStateChoice[] = [
  "AK",
  "AL",
  "AS",
  "AZ",
  "AR",
  "CA",
  "CO",
  "CT",
  "DE",
  "DC",
  "FL",
  "GA",
  "GU",
  "HI",
  "ID",
  "IL",
  "IN",
  "IA",
  "KS",
  "KY",
  "LA",
  "ME",
  "MD",
  "MA",
  "MI",
  "MN",
  "MP",
  "MS",
  "MO",
  "MT",
  "NE",
  "NV",
  "NH",
  "NJ",
  "NM",
  "NY",
  "NC",
  "ND",
  "OH",
  "OK",
  "OR",
  "PA",
  "PR",
  "RI",
  "SC",
  "SD",
  "TN",
  "TX",
  "UT",
  "VT",
  "VA",
  "VI",
  "WA",
  "WV",
  "WI",
  "WY"
];

const USStateChoiceSet: Set<String> = new Set(USStateChoices);

export function isUSStateChoice(choice: string): choice is USStateChoice {
  return USStateChoiceSet.has(choice);
}

export type USStateChoiceLabels = {
  [k in USStateChoice]: string;
};

export function getUSStateChoiceLabels(): USStateChoiceLabels {
  return {
    AK: "Alaska",
    AL: "Alabama",
    AS: "American Samoa",
    AZ: "Arizona",
    AR: "Arkansas",
    CA: "California",
    CO: "Colorado",
    CT: "Connecticut",
    DE: "Delaware",
    DC: "District of Columbia",
    FL: "Florida",
    GA: "Georgia",
    GU: "Guam",
    HI: "Hawaii",
    ID: "Idaho",
    IL: "Illinois",
    IN: "Indiana",
    IA: "Iowa",
    KS: "Kansas",
    KY: "Kentucky",
    LA: "Louisiana",
    ME: "Maine",
    MD: "Maryland",
    MA: "Massachusetts",
    MI: "Michigan",
    MN: "Minnesota",
    MP: "Northern Mariana Islands",
    MS: "Mississippi",
    MO: "Missouri",
    MT: "Montana",
    NE: "Nebraska",
    NV: "Nevada",
    NH: "New Hampshire",
    NJ: "New Jersey",
    NM: "New Mexico",
    NY: "New York",
    NC: "North Carolina",
    ND: "North Dakota",
    OH: "Ohio",
    OK: "Oklahoma",
    OR: "Oregon",
    PA: "Pennsylvania",
    PR: "Puerto Rico",
    RI: "Rhode Island",
    SC: "South Carolina",
    SD: "South Dakota",
    TN: "Tennessee",
    TX: "Texas",
    UT: "Utah",
    VT: "Vermont",
    VA: "Virginia",
    VI: "Virgin Islands",
    WA: "Washington",
    WV: "West Virginia",
    WI: "Wisconsin",
    WY: "Wyoming",
  };
}
