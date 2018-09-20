import React from 'react';

import { DetailedHTMLProps, AnchorHTMLAttributes, MouseEvent } from "react";
import { Omit, callOnceWithinMs, getFunctionProperty } from "./util";
import hardRedirect from './tests/hard-redirect';

/**
 * The analytics.js API is provided by Google Analytics:
 * 
 *   https://developers.google.com/analytics/devguides/collection/analyticsjs/
 * 
 * Here we only define the parts of it that we use.
 */
export interface GoogleAnalyticsAPI {
  // https://developers.google.com/analytics/devguides/collection/analyticsjs/single-page-applications
  (cmd: 'set', fieldName: 'page', fieldValue: string): void;
  (cmd: 'send', hitType: 'pageview'): void;
  // https://support.google.com/analytics/answer/1136920?hl=en
  (cmd: 'send', hitType: 'event', eventCategory: 'outbound', eventAction: 'click', url: string, fields: {
    transport: 'beacon',
    hitCallback: () => void
  }): void;
};

declare global {
  interface Window {
    /**
     * A reference to the ga() global function, provided by analytics.js.
     *
     * However, it won't exist if the app hasn't been configured to support GA.
     */
    ga: GoogleAnalyticsAPI|undefined;
  }
}

/**
 * For the most part, ga() is just a "fire and forget" function,
 * but sometimes we need to pass it callbacks that it calls
 * after it's registered a "hit" with GA. When we don't actually
 * have GA configured, though, we want to simulate this
 * behavior, so the following helper can be used to call
 * any hit callbacks that have been passed to our ga() stub.
 */
function callAnyHitCallbacks(args: unknown[]) {
  for (let arg of args) {
    const hitCallback = getFunctionProperty(arg, 'hitCallback');
    if (hitCallback) {
      setTimeout(hitCallback, 0);
    }
  }
}

/** 
 * A safe reference to a GA API we can use. If GA isn't configured,
 * this is largely a no-op.
 */
export const ga: GoogleAnalyticsAPI = function ga() {
  if (typeof(window) !== 'undefined' && typeof(window.ga) === 'function') {
    window.ga.apply(window, arguments);
  } else {
    callAnyHitCallbacks(Array.from(arguments));
  }
};

/**
 * Track a virtual page view in our single-page application.
 *
 * @param pathname The new page the user has arrived at.
 */
export function trackPageView(pathname: string) {
  ga('set', 'page', pathname);
  ga('send', 'pageview');
}

/**
 * When we call ga(), it's actually possible that GA never loaded,
 * and window.ga is just the stub in the GA snippet that came with
 * our page. There are other potential edge cases where our
 * hit callback might never be called, so let's ensure that we
 * navigate regardless once the given number of milliseconds
 * have elapsed, just to be safe.
 */
const OUTBOUND_LINK_TIMEOUT_MS = 1000;

/** An event handler executed when a user clicks on an outbound link. */
export function handleOutboundLinkClick(e: MouseEvent<HTMLAnchorElement>) {
  // If any modifier key is pressed, odds are that the user is trying to
  // invoke some browser-specific behavior to e.g. open the link in a
  // new window or tab. We don't want to break that.
  const isModifierPressed = e.altKey || e.ctrlKey || e.metaKey || e.shiftKey;

  if (!isModifierPressed) {
    const { href, target } = e.currentTarget;

    ga('send', 'event', 'outbound', 'click', href, {
      transport: 'beacon',
      hitCallback: callOnceWithinMs(() => {
        if (target) {
          window.open(href, target);
        } else {
          hardRedirect(href);
        }
      }, OUTBOUND_LINK_TIMEOUT_MS)
    });
    e.preventDefault();
  }
}

type OutboundLinkProps = Omit<DetailedHTMLProps<AnchorHTMLAttributes<HTMLAnchorElement>, HTMLAnchorElement> & {
  /** The "href" prop is required on outbound links, not optional. */
  href: string;
}, 'onClick'>;

/**
 * A react component that encapsulates a link to an external website,
 * which we want to track with analytics.
 */
export function OutboundLink(props: OutboundLinkProps): JSX.Element {
  return <a {...props} onClick={handleOutboundLinkClick}>{props.children}</a>;
}
