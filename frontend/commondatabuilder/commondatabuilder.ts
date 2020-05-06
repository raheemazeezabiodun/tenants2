import * as fs from "fs";
import * as path from "path";

import { DjangoChoices } from "../lib/common-data";

export type DjangoChoicesTypescriptConfig = {
  /** The root directory from which to read JSON files and write TS files. */
  rootDir: string;

  /** The files to convert from JSON to TS. */
  files: DjangoChoicesTypescriptFileConfig[];
};

export type DjangoChoicesTypescriptFileConfig = {
  /** The JSON file to convert to TS. */
  jsonFilename: string;

  /** The name of the TS type to generate. */
  typeName: string;

  /** Whether to export the labels in the JSON file to TS. */
  exportLabels: boolean;

  /** Whether to internationalize the labels in the JSON file. */
  internationalizeLabels?: boolean;

  /**
   * Filter out the given values from either the given list of choices, or anything
   * that matches the given regular expression.
   */
  filterOut?: RegExp | string[];
};

/**
 * Retrieve the human-readable label for a choice, given its machine-readable value.
 *
 * Return null if the choice is invalid.
 */
export function safeGetDjangoChoiceLabel(
  choices: DjangoChoices,
  value: string
): string | null {
  for (let [v, label] of choices) {
    if (v === value) return label;
  }
  return null;
}

/**
 * Validate that the given values are valid choices.
 *
 * This is intended to be used in tests. It should be removed from
 * production bundles via tree-shaking.
 */
export function validateDjangoChoices(
  choices: DjangoChoices,
  values: string[]
) {
  values.forEach((value) => {
    getDjangoChoiceLabel(choices, value);
  });
}

/**
 * Filter out the given values from either the given list of choices, or anything
 * that matches the given regular expression.
 */
export function filterDjangoChoices(
  choices: DjangoChoices,
  values: string[] | RegExp
): DjangoChoices {
  if (Array.isArray(values)) {
    validateDjangoChoices(choices, values);
    return choices.filter(([value, _]) => !values.includes(value));
  } else {
    return choices.filter(([value, _]) => !values.test(value));
  }
}

/**
 * Retrieve the human-readable label for a choice, given its machine-readable value.
 *
 * Throw an exception if the choice is invalid.
 */
export function getDjangoChoiceLabel(
  choices: DjangoChoices,
  value: string
): string {
  const result = safeGetDjangoChoiceLabel(choices, value);
  if (result === null) {
    throw new Error(`Unable to find label for value ${value}`);
  }
  return result;
}

function replaceExt(filename: string, ext: string) {
  // https://stackoverflow.com/a/5953384
  return filename.substr(0, filename.lastIndexOf(".")) + ext;
}

type DjangoChoiceTypescriptFile = {
  tsPath: string;
  ts: string;
};

export function createDjangoChoicesTypescriptFiles(
  config: DjangoChoicesTypescriptConfig,
  dryRun: boolean = false
): DjangoChoiceTypescriptFile[] {
  return config.files.map((fileConfig) => {
    const infile = path.join(config.rootDir, fileConfig.jsonFilename);
    let choices = JSON.parse(
      fs.readFileSync(infile, {
        encoding: "utf-8",
      })
    ) as DjangoChoices;
    if (fileConfig.filterOut) {
      choices = filterDjangoChoices(choices, fileConfig.filterOut);
    }
    const ts = createDjangoChoicesTypescript(choices, fileConfig.typeName, {
      exportLabels: fileConfig.exportLabels,
      internationalizeLabels: fileConfig.internationalizeLabels,
    });
    const tsFilename = replaceExt(fileConfig.jsonFilename, ".ts");
    const tsPath = path.join(config.rootDir, tsFilename);
    if (!dryRun) {
      console.log(`Writing ${tsFilename}.`);
      fs.writeFileSync(tsPath, ts, { encoding: "utf-8" });
    }
    return { tsPath, ts };
  });
}

function createInternationalizedStringLiteral(value: string): string {
  const backtickedValue = "`" + JSON.stringify(value).slice(1, -1) + "`";
  return `li18n._(t${backtickedValue})`;
}

/**
 * Return a list of TypeScript lines that create a function
 * which returns a mapping from choice values to their labels.
 *
 * Note that this is a function rather than a constant because
 * we need to localize the labels at runtime if needed.
 */
function createLabelExporter(
  choices: DjangoChoices,
  name: string,
  options: CreateOptions
): string[] {
  const lines = [];
  lines.push(
    `export type ${name}Labels = {`,
    `  [k in ${name}]: string;`,
    `};\n`
  );
  lines.push(
    `export function get${name}Labels(): ${name}Labels {`,
    `  return {`
  );
  for (let [name, label] of choices) {
    const value = options.internationalizeLabels
      ? createInternationalizedStringLiteral(label)
      : JSON.stringify(label);
    lines.push(`    ${name}: ${value},`);
  }
  lines.push("  };", "}\n");
  return lines;
}

type CreateOptions = {
  exportLabels: boolean;
  internationalizeLabels: boolean;
};

const defaultOptions: CreateOptions = {
  exportLabels: true,
  internationalizeLabels: false,
};

/**
 * Return a list of TypeScript lines that define a type
 * and some helper functions for the given Django choices.
 */
export function createDjangoChoicesTypescript(
  choices: DjangoChoices,
  name: string,
  options: Partial<CreateOptions> = {}
): string {
  const finalOptions = Object.assign({}, defaultOptions, options);
  const { exportLabels, internationalizeLabels } = finalOptions;
  const lines = [
    `// This file was auto-generated by commondatabuilder.`,
    `// Please don't edit it.\n`,
  ];
  if (exportLabels && internationalizeLabels) {
    lines.push(`import { t } from "@lingui/macro";`);
    lines.push(`import { li18n } from '../frontend/lib/i18n-lingui';\n`);
  }
  const choiceKeys = choices.map((choice) => choice[0]);
  const quotedChoiceKeys = choiceKeys.map((key) => JSON.stringify(key));
  lines.push(`export type ${name} = ${quotedChoiceKeys.join("|")};\n`);
  lines.push(
    `export const ${name}s: ${name}[] = ${JSON.stringify(
      choiceKeys,
      null,
      2
    )};\n`
  );
  lines.push(`const ${name}Set: Set<String> = new Set(${name}s);\n`);
  lines.push(
    `export function is${name}(choice: string): choice is ${name} {`,
    `  return ${name}Set.has(choice);`,
    `}\n`
  );
  if (exportLabels) {
    lines.push(...createLabelExporter(choices, name, finalOptions));
  }
  return lines.join("\n");
}
