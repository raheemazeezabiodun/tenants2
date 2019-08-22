import React from 'react';

export function whoOwnsWhatURL(bbl: string): string {
  return `https://whoownswhat.justfix.nyc/bbl/${bbl}`;
}

export function WhoOwnsWhatLink(props: {bbl: string, className?: string, children: any}): JSX.Element {
  return <a
    href={whoOwnsWhatURL(props.bbl)}
    target="_blank"
    rel="noopener noreferrer"
    className={props.className}
  >{props.children}</a>;
}