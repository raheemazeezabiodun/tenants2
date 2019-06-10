import * as fs from 'fs';
import * as path from 'path';
import glob from 'glob';

import { getGraphQlFragments, strContains, ToolError, writeFileIfChangedSync } from './util';
import { APOLLO_GEN_PATH, QUERIES_PATH, DOT_GRAPHQL, QUERIES_GLOB } from './config';

/**
 * This class is responsible for taking a raw text
 * GraphQL query/mutation/fragment, Apollo codegen:generate'd TypeScript
 * interfaces for it, and combining them. In the case of
 * queries and mutations, we also generate
 * a strongly-typed TS function that wraps the query.
 * 
 * This is partially based on the following blog post,
 * thought it went an extra step to convert the raw
 * text query into an AST, which is way beyond what
 * we need right now, and also way beyond my current
 * understanding of GraphQL:
 * 
 * https://medium.com/@crucialfelix/bridging-the-server-client-gap-graphql-typescript-and-apollo-codegen-e5b54fa96ae2
 */
export class GraphQlFile {
  /** The name of the GraphQL query filename, without its directory. */
  graphQlFilename: string;

  /** The base name of the GraphQL query filename, without its extension. */
  basename: string;

  /** The raw GraphQL query. */
  graphQl: string;

  /** The path to the TypeScript code that implements our generated function. */
  tsCodePath: string;

  /** The path to the file containing the raw GraphQL query. */
  graphQlPath: string;

  /** The filename of the Apollo codegen:generate'd Typescript interfaces for the query. */
  tsInterfacesFilename: string;

  /** The path to the Apollo codegen:generate'd Typescript interfaces for the query. */
  tsInterfacesPath: string;

  /** External fragments that the GraphQL refers to, if any. */
  fragments: string[];

  constructor(readonly fullPath: string, genPath: string = APOLLO_GEN_PATH) {
    this.graphQlFilename = path.basename(fullPath);
    this.basename = path.basename(this.graphQlFilename, DOT_GRAPHQL);
    this.graphQlPath = fullPath;
    this.graphQl = fs.readFileSync(fullPath, { encoding: 'utf-8' });
    this.tsInterfacesFilename = `${this.basename}.ts`;
    this.tsInterfacesPath = path.join(genPath, this.tsInterfacesFilename);
    this.tsCodePath = path.join(QUERIES_PATH, `${this.basename}.ts`);
    this.fragments = getGraphQlFragments(this.graphQl);
  }

  /** Returns whether our GraphQL contains any of the given strings. */
  graphQlContains(...strings: string[]): boolean {
    return strContains(this.graphQl, ...strings);
  }

  /**
   * Generates an ES6 template literal that, when evaluated in the
   * proper context, is the text of our source GraphQL file, along
   * with all dependencies (e.g. fragments).
   **/
  getGraphQlTemplateLiteral(): string {
    const parts = [this.graphQl];

    this.fragments.forEach(fragmentName => {
      parts.push('${' + fragmentName + '.graphQL}');
    });

    return '`' + parts.join('\n') + '`';
  }

  /**
   * Returns the comments and imports that should appear at the
   * beginning of our generated TypeScript code.
   */
  getTsCodeHeader(): string {
    const lines = [
      '// This file was automatically generated and should not be edited.\n'
    ];

    this.fragments.forEach(fragmentName => {
      lines.push(`import * as ${fragmentName} from './${fragmentName}'`);
    });

    return lines.join('\n');
  }

  /** Generate the TypeScript code that clients will use. */
  generateTsCode(): string {
    if (this.graphQl.indexOf(this.basename) === -1) {
      throw new ToolError(`Expected ${this.graphQlFilename} to define "${this.basename}"!`);
    }

    if (this.graphQlContains(`mutation ${this.basename}`, `query ${this.basename}`)) {
      return this.generateTsCodeForQueryOrMutation();
    } else if (this.graphQlContains(`fragment ${this.basename}`)) {
      return this.generateTsCodeForFragment();
    } else {
      throw new ToolError(`${this.basename} is an unrecognized GraphQL type`);
    }
  }

  /** Return the TypeScript interfaces code created by Apollo codegen:generate. */
  getTsInterfaces(): string {
    if (!fs.existsSync(this.tsInterfacesPath)) {
      throw new ToolError(`Expected ${this.tsInterfacesPath} to exist!`);
    }

    const tsInterfaces = fs.readFileSync(this.tsInterfacesPath, { encoding: 'utf-8' });

    if (tsInterfaces.indexOf(this.basename) === -1) {
      throw new ToolError(`Expected ${this.tsInterfacesFilename} to define "${this.basename}"!`);
    }

    return tsInterfaces;
  }

  /** Generate the TypeScript code when our file is a GraphQL fragment. */
  generateTsCodeForFragment(): string {
    return [
      this.getTsCodeHeader(),
      this.getTsInterfaces(),
      `export const graphQL = ${this.getGraphQlTemplateLiteral()};`
    ].join('\n');
  }

  /**
   * Generate the TypeScript code when our file is a GraphQL
   * query or mutation.
   */
  generateTsCodeForQueryOrMutation(): string {
    const tsInterfaces = this.getTsInterfaces();
    let variablesInterfaceName = `${this.basename}Variables`;
    let args = '';

    if (tsInterfaces.indexOf(variablesInterfaceName) !== -1) {
      args = `args: ${variablesInterfaceName}`;
    }

    const fetchGraphQL = 'fetchGraphQL: (query: string, args?: any) => Promise<any>';

    return [
      this.getTsCodeHeader(),
      tsInterfaces,
      `export const ${this.basename} = {`,
      `  // The following query was taken from ${this.graphQlFilename}.`,
      `  graphQL: ${this.getGraphQlTemplateLiteral()},`,
      `  fetch(${fetchGraphQL}, ${args}): Promise<${this.basename}> {`,
      `    return fetchGraphQL(${this.basename}.graphQL${args ? ', args' : ''});`,
      `  }`,
      `};`,
      ``,
      `export const fetch${this.basename} = ${this.basename}.fetch;`
    ].join('\n');
  }

  /** Write out our TypeScript code to a file. */
  writeTsCode(extraCode?: string): boolean {
    extraCode = extraCode ? '\n\n' + extraCode : '';
    return writeFileIfChangedSync(this.tsCodePath, this.generateTsCode() + extraCode);
  }

  /** Scan the directory containing our GraphQL queries. */
  static fromDir() {
    return glob.sync(QUERIES_GLOB).map(fullPath => new GraphQlFile(fullPath));
  }
}
